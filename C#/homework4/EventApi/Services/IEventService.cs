namespace EventApi.Services
{
    interface IEventService
    {
        public object CreateEvent(Event newEvent);
        public object DeleteEvent(int toDelete);
        public object GetEvent(int toGet);
        public object EditEvent(int toGet, Event newEvent);
        public object GetEvents(string toFind, string sort_param, string sort_type, int limit, int offset);
    }
}
