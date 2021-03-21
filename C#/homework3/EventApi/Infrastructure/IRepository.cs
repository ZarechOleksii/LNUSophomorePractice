using System;
using System.Collections.Generic;
using System.Linq;
using System.Threading.Tasks;

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
