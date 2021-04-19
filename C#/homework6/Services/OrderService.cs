using System;
using System.Collections.Generic;
using System.Linq;
using System.Threading.Tasks;

namespace EventApi.Services
{
    public class OrderService : IOrderService
    {
        private readonly Repository<Order> rep = new(new PGContext());

        public object GetAll()
        {
            var all = rep.FetchAll();
            return new OKAllOutput<Order> { Status = 200, Message = "Success", Amount = all.Count, Result = all };
        }
        public object GetOrdersOfUser(string email)
        {
            var all = rep.FetchAll().Where(a => a.Person_Email == email).ToList();
            return new OKAllOutput<Order> { Status = 200, Message = "Success", Amount = all.Count, Result = all };
        }
        public object GetOrderById(string email, int id)
        {
            var all = rep.FetchAll().FirstOrDefault(a => a.Person_Email == email && a.Id == id);
            if (all == null)
                return new NotFoundOutput { Status = 404, Message = "You do not have order with such id" };
            return new OKOutput<Order> { Status = 200, Message = "Success", Result = all };
        }
        public object AddOrder(string email, RequestModels.NewOrder newOrder)
        {
            if (newOrder == null)
                return new BadRequestOutput { Message = "Order is null", Status = 400 };
            Repository<Event> repEvent = new(new PGContext());
            Event ofOrder = repEvent.GetT(new object[] { newOrder.Event_Id });
            if (ofOrder == null)
                return new NotFoundOutput { Message = "No event with such id", Status = 404 };
            if (ofOrder.Amount < newOrder.Amount)
                return new BadRequestOutput { Message = "Not enough in stock", Status = 400 };
            Event newEventValue = new() { Id = ofOrder.Id, DateTime = ofOrder.DateTime, Title = ofOrder.Title, 
                Price = ofOrder.Price, Duration = ofOrder.Duration, RestName= ofOrder.RestName, Amount = ofOrder.Amount - newOrder.Amount };
            repEvent.Update(ofOrder, newEventValue);
            repEvent.Save();
            rep.LogUser(email);
            var toAdd = new Order { Amount = newOrder.Amount, DateTime = DateTime.Now, Event_Id = newOrder.Event_Id, Person_Email = email };
            rep.Add(toAdd);
            rep.Save();
            rep.LogUser(email);
            return new OKOutput<Order> { Status = 200, Message = "Success", Result = toAdd };
        }
        public object GetOrderByIdAdmin(int id)
        {
            var all = rep.FetchAll().FirstOrDefault(a => a.Id == id);
            if (all == null)
                return new NotFoundOutput { Status = 404, Message = "No order with such id" };
            return new OKOutput<Order> { Status = 200, Message = "Success", Result = all };
        }
    }
}
