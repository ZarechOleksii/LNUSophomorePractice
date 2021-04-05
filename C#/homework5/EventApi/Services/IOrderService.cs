using System;
using System.Collections.Generic;
using System.Linq;
using System.Threading.Tasks;

namespace EventApi.Services
{
    interface IOrderService
    {
        public object GetAll();
        public object GetOrdersOfUser(string email);
        public object GetOrderById(string email, int id);
        public object AddOrder(string email, RequestModels.NewOrder newOrder);
        public object GetOrderByIdAdmin(int id);
    }
}
