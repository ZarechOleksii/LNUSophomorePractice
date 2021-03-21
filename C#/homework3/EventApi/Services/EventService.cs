using Microsoft.EntityFrameworkCore;
using System;
using System.Collections.Generic;
using System.Linq;
using System.Reflection;
using System.Threading.Tasks;

namespace EventApi.Services
{
    public class EventService : IEventService
    {
        private readonly Repository rep = new(new PGContext());
        public Dictionary<string, dynamic> GetEvents(string toFind, string sort_param, string sort_type, int limit, int offset)
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
                if (typeof(Event).GetProperty(sort_param, BindingFlags.IgnoreCase | BindingFlags.Public | BindingFlags.Instance) != null)
                    all = all.OrderBy(x => typeof(Event).GetProperty(sort_param, BindingFlags.IgnoreCase | BindingFlags.Public | BindingFlags.Instance).GetValue(x)).ToList();
            if (sort_type != null)
                if (sort_type.ToLower() == "desc")
                    all.Reverse();

            if (limit > 0)
            {
                if (offset > 0)
                {
                    if ((offset * limit) >= all.Count)
                        return new Dictionary<string, dynamic> { { "status", 404 }, { "message", "no events to display here" } };
                }
                else
                    offset = 0;
                if ((offset * limit) + limit > all.Count)
                    all = all.GetRange(offset * limit, all.Count - (offset * limit));
                else
                    all = all.GetRange(offset * limit, limit);
            }

            return new Dictionary<string, dynamic> { { "status", 200 }, { "message", "success" }, { "amount", all.Count }, { "events", all } };
        }

        public Dictionary<string, dynamic> CreateEvent(Event newEvent)
        {
            if (newEvent == null)
                return new Dictionary<string, dynamic> { { "status", 400 }, { "message", "new event is null" } };

            Event inBase = rep.GetEvent(newEvent.Id);
            if (inBase != null)
                return new Dictionary<string, dynamic> { { "status", 400 }, { "message", "event with this id already exists" } };

            rep.Add(newEvent);
            rep.Save();
            return new Dictionary<string, dynamic> { { "status", 200 }, { "message", "success" }, { "event", newEvent } };
        }
        public Dictionary<string, dynamic> GetEvent(int eventId)
        {
            Event inBase = rep.GetEvent(eventId);
            if (inBase == null)
                return new Dictionary<string, dynamic> { { "status", 404 }, { "message", "event with this id does not exist" } };

            return new Dictionary<string, dynamic> { { "status", 200 }, { "message", "success" }, { "event", inBase } };
        }
        public Dictionary<string, dynamic> DeleteEvent(int eventId)
        {
            Event inBase = rep.GetEvent(eventId);
            if (inBase == null)
                return new Dictionary<string, dynamic> { { "status", 404 }, { "message", "event with this id does not exist" } };

            rep.Delete(inBase);
            rep.Save();
            return new Dictionary<string, dynamic> { { "status", 200 }, { "message", "success" } };
        }
        public Dictionary<string, dynamic> EditEvent(int eventId, Event newEvent)
        {
            if (newEvent == null)
                return new Dictionary<string, dynamic> { { "status", 400 }, { "message", "event is null" } };

            Event inBase = rep.GetEvent(eventId);
            if (inBase == null)
                return new Dictionary<string, dynamic> { { "status", 404 }, { "message", "event with this id does not exist" } };

            newEvent.Id = eventId;
            rep.Edit(newEvent);
            rep.Save();
            return new Dictionary<string, dynamic> { {"status", 200 }, { "message", "success" }, { "event", newEvent} };
        }
    }
}
