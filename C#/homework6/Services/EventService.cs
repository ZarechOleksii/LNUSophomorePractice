using System.Collections.Generic;
using System.Linq;
using System.Reflection;

namespace EventApi.Services
{
    public class EventService : IEventService
    {
        private readonly Repository<Event> rep = new(new PGContext());
        public object GetEvents(string toFind, string sort_param, string sort_type, int limit, int offset)
        {
            List<Event> all = rep.FetchAll();
            int amount = all.Count;
            if (toFind != null)
                all = all.Where(x =>
                   x.Title.ToString().ToLower().Contains(toFind.ToLower())
                || x.Duration.ToString().ToLower().Contains(toFind.ToLower())
                || x.DateTime.ToString().ToLower().Contains(toFind.ToLower())
                || x.Price.ToString().ToLower().Contains(toFind.ToLower())
                || x.RestName.ToString().ToLower().Contains(toFind.ToLower())
                ).ToList();

            if (sort_param != null)
            {
                if (typeof(Event).GetProperty(sort_param, BindingFlags.IgnoreCase | BindingFlags.Public | BindingFlags.Instance) != null)
                    all = all.OrderBy(x => typeof(Event).GetProperty(sort_param, BindingFlags.IgnoreCase | BindingFlags.Public | BindingFlags.Instance).GetValue(x)).ToList();
                else
                    return new BadRequestOutput { Message = "No such sort parameter", Status = 400 };
            }
            if (sort_type != null)
                if (sort_type.ToLower() == "desc")
                    all.Reverse();

            if (limit > 0)
            {
                if (offset > 0)
                {
                    if ((offset * limit) >= all.Count)
                        return new NotFoundOutput { Message = "No events on this page", Status = 404 };
                }
                else
                    offset = 0;
                if ((offset * limit) + limit > all.Count)
                    all = all.GetRange(offset * limit, all.Count - (offset * limit));
                else
                    all = all.GetRange(offset * limit, limit);
            }
            return new OKAllOutput<Event> { Message = "Success", Status = 200, Amount = amount, Result = all };
        }

        public object CreateEvent(string email, Event newEvent)
        {
            if (newEvent == null)
                return new BadRequestOutput { Message = "Event is null", Status = 400 };

            Event inBase = rep.GetT(new object[] { newEvent.Id });
            if (inBase != null)
                return new BadRequestOutput { Message = "Event with this id already exists", Status = 400 };

            rep.Add(newEvent);
            rep.Save();
            rep.LogUser(email);
            return new OKOutput<Event> { Message = "Success", Status = 200, Result = newEvent };
        }
        public object GetEvent(int eventId)
        {
            Event inBase = rep.GetT(new object[] { eventId });
            if (inBase == null)
                return new NotFoundOutput { Message = "Event with this id does not exist", Status = 404 };

            return new OKOutput<Event> { Message = "Success", Status = 200, Result = inBase };
        }
        public object DeleteEvent(string email, int eventId)
        {
            Event inBase = rep.GetT(new object[] { eventId });
            if (inBase == null)
                return new NotFoundOutput { Message = "Event with this id does not exist", Status = 404 };

            rep.Delete(inBase);
            rep.Save();
            rep.LogUser(email);
            return new OKOutput<Event> { Message = "Success", Status = 200, Result = inBase };
        }
        public object EditEvent(string email, int eventId, Event newEvent)
        {
            if (newEvent == null)
                return new BadRequestOutput { Message = "Event is null", Status = 400 };

            Event inBase = rep.GetT(new object[] { eventId });
            if (inBase == null)
                return new NotFoundOutput { Message = "Event with this id does not exist", Status = 404 };

            newEvent.Id = eventId;
            rep.Update(inBase, newEvent);
            rep.Save();
            rep.LogUser(email);
            return new OKOutput<Event> { Message = "Success", Status = 200, Result = newEvent };
        }
    }
}
