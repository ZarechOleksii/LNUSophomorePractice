using Microsoft.EntityFrameworkCore;
using System.Collections.Generic;
using System.Linq;

namespace EventApi
{
    public class Repository<TEntity> where TEntity : class
    {
        readonly PGContext db;
        readonly DbSet<TEntity> dbSet;
        public Repository(PGContext db)
        {
            this.db = db;
            dbSet = db.Set<TEntity>();
        }

        public List<TEntity> FetchAll()
        {
            return dbSet.AsNoTracking().ToList();
        }

        public void Add(TEntity entity)
        {
            dbSet.Add(entity);
        }

        public void Delete(TEntity entity)
        {
            dbSet.Remove(entity);
        }
        public void Update(TEntity old, TEntity entity)
        {
            db.Entry(old).CurrentValues.SetValues(entity);
        }
        public TEntity GetT(object[] entity)
        {
            TEntity toReturn = dbSet.Find(entity);
            return toReturn;
        }
        public bool Present(object[] entity)
        {
            TEntity toReturn = dbSet.Find(entity);
            if (toReturn == null)
                return false;
            db.Entry(toReturn).State = EntityState.Detached;
            return true;
        }
        public void Save()
        {
            db.SaveChanges();
        }
    }
}
