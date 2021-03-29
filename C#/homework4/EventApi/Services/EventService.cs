using System.Collections.Generic;
using System.Linq;
using System.Reflection;

namespace EventApi.Services
{
    public class EventService : IEventService
    {
        private readonly Repository rep = new(new PGContext());
        public object GetEvents(string toFind, string sort_param, string sort_type, int limit, int offset)
        {

            List<Event> all = rep.FetchAll();
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
            return new OKAllOutput { Message = "Success", Status = 200, Amount = all.Count, Events = all };
        }

        public object CreateEvent(Event newEvent)
        {
            if (newEvent == null)
                return new BadRequestOutput { Message = "Event is null", Status = 400 };

            Event inBase = rep.GetEvent(newEvent.Id);
            if (inBase != null)
                return new BadRequestOutput { Message = "Event with this id already exists", Status = 400 };

            rep.Add(newEvent);
            rep.Save();
            return new OKOutput { Message = "Success", Status = 200, Event = newEvent };
        }
        public object GetEvent(int eventId)
        {
            Event inBase = rep.GetEvent(eventId);
            if (inBase == null)
                return new NotFoundOutput { Message = "Event with this id does not exist", Status = 404 };

            return new OKOutput { Message = "Success", Status = 200, Event = inBase };
        }
        public object DeleteEvent(int eventId)
        {
            Event inBase = rep.GetEvent(eventId);
            if (inBase == null)
                return new NotFoundOutput { Message = "Event with this id does not exist", Status = 404 };

            rep.Delete(inBase);
            rep.Save();
            return new OKOutput { Message = "Success", Status = 200, Event = inBase };
        }
        public object EditEvent(int eventId, Event newEvent)
        {
            if (newEvent == null)
                return new BadRequestOutput { Message = "Event is null", Status = 400 };

            Event inBase = rep.GetEvent(eventId);
            if (inBase == null)
                return new NotFoundOutput { Message = "Event with this id does not exist", Status = 404 };

            newEvent.Id = eventId;
            rep.Edit(newEvent);
            rep.Save();
            return new OKOutput { Message = "Success", Status = 200, Event = newEvent };
        }
    }
}
