namespace EventApi.Services
{
    interface IEventService
    {
        public object CreateEvent(string email, Event newEvent);
        public object DeleteEvent(string email, int toDelete);
        public object GetEvent(int toGet);
        public object EditEvent(string email, int toGet, Event newEvent);
        public object GetEvents(string toFind, string sort_param, string sort_type, int limit, int offset);
    }
}
