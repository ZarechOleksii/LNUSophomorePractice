using System.Collections.Generic;

namespace EventApi
{
    public interface IRepository
    {
        List<Event> FetchAll();
        void Add(Event entity);
        void Delete(Event entity);
        void Edit(Event entity);
        void Save();
        Event GetEvent(int entity);
        void Execute(string input);
    }
}
