using System;
using System.Collections.Generic;
using System.Linq;
using System.Threading.Tasks;

namespace EventApi.Services
{
    interface IEventService
    {
        public Dictionary<string, dynamic> CreateEvent(Event newEvent);
        public Dictionary<string, dynamic> DeleteEvent(int toDelete);
        public Dictionary<string, dynamic> GetEvent(int toGet);
        public Dictionary<string, dynamic> EditEvent(int toGet, Event newEvent);
        public Dictionary<string, dynamic> GetEvents(string toFind, string sort_param, string sort_type, int limit, int offset);
    }
}
