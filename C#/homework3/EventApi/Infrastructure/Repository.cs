using Microsoft.EntityFrameworkCore;
using System;
using System.Collections.Generic;
using System.Linq;

namespace EventApi
{
    public class Repository : IRepository
    {
        PGContext db;
        public Repository(PGContext db)
        {
            this.db = db;
        }
        public void Execute(string input)
        {
            db.Database.ExecuteSqlRaw(input);
        }
        public List<Event> FetchAll()
        {
            return db.Events.ToList();
        }

        public void Add(Event entity)
        {
            db.Events.Add(entity);
        }

        public void Delete(Event entity)
        {
            db.Remove(entity);
        }
        public void Edit(Event entity)
        {
            var given = db.Events.Find(entity.Id);
            db.Entry(given).CurrentValues.SetValues(entity);
        }
        public Event GetEvent(int entity)
        {
            Event toReturn = db.Events.Find(entity);
            return toReturn;
        }
        public void Save()
        {
            db.SaveChanges();
        }
    }
}
