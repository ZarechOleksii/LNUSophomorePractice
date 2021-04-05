using EventApi.Services;
using Microsoft.AspNetCore.Authorization;
using Microsoft.AspNetCore.Mvc;
using System;
using System.Collections.Generic;
using System.Linq;
using System.Security.Claims;
using System.Threading.Tasks;
using static EventApi.RequestModels;

namespace EventApi.Controllers
{
    [Produces("application/json")]
    [ApiController]
    [Authorize]
    public class OrderController : Controller
    {
        private readonly OrderService service = new();

        /// <summary>
        /// Fetches all orders
        /// </summary>
        /// <returns> 200 response code, success message, amount of separate orders, and found Orders </returns>
        /// <response code="200"> Successfully found </response>
        [Authorize(Roles = "Admin")]
        [Route("/admin/orders")]
        [HttpGet]
        [ProducesResponseType(typeof(OKAllOutput<Order>), 200)]
        public IActionResult GetAllOrders()
        {
            return Returning(service.GetAll());
        }

        /// <summary>
        /// Fetches one order by id
        /// </summary>
        /// <param name="id" example="1">Id of order to find</param> 
        /// <returns> 200 response code, success message, and found Order </returns>
        /// <response code="404"> Order with this id was not found </response>   
        /// <response code="200"> Successfully found </response>
        [Authorize(Roles = "Admin")]
        [Route("/admin/orders/{id}")]
        [HttpGet]
        [ProducesResponseType(typeof(OKOutput<Order>), 200)]
        [ProducesResponseType(typeof(NotFoundOutput), 404)]
        public IActionResult GetOrderByIdAdmin(int id)
        {
            return Returning(service.GetOrderByIdAdmin(id));
        }
        /// <summary>
        /// Fetches all orders of current user
        /// </summary>
        /// <returns> 200 response code, success message, amount of separate orders, and found Orders </returns>
        /// <response code="200"> Successfully found </response>
        [Route("orders")]
        [HttpGet]
        [ProducesResponseType(typeof(OKAllOutput<Order>), 200)]
        public IActionResult GetUserOrders()
        {
            string email = GetEmail(User.Claims);
            return Returning(service.GetOrdersOfUser(email));
        }

        /// <summary>
        /// Fetches one order of current user by Id
        /// </summary>
        /// <param name="id" example="1">Id of order to find</param> 
        /// <returns> 200 response code, success message, and found Order </returns>
        /// <response code="404"> Order with this id was not found </response> 
        /// <response code="200"> Successfully found </response>
        [Route("orders/{id}")]
        [HttpGet]
        [ProducesResponseType(typeof(OKOutput<Order>), 200)]
        [ProducesResponseType(typeof(NotFoundOutput), 404)]
        public IActionResult GetUserOrderById(int id)
        {
            string email = GetEmail(User.Claims);
            return Returning(service.GetOrderById(email, id));
        }
        /// <summary>
        /// Creates a new Order
        /// </summary>
        /// <param name="newOrder">New order data</param> 
        /// <remarks>
        /// Sample request:
        ///
        ///     POST
        ///     {
        ///        "event_id": 1,
        ///        "amount": 1
        ///     }
        ///
        /// </remarks>
        /// <returns> 200 response code, success message and created Order </returns>
        /// <response code="200"> Success </response>
        /// <response code="400"> Order is null / Order does not pass validation / Not enough in stock </response> 
        /// <response code="404"> No such event to order </response> 
        [Route("orders")]
        [HttpPost]
        [ProducesResponseType(typeof(OKOutput<Order>), 200)]
        [ProducesResponseType(typeof(NotFoundOutput), 404)]
        [ProducesResponseType(typeof(BadRequestOutput), 400)]
        public IActionResult AddOrder(NewOrder newOrder)
        {
            string email = GetEmail(User.Claims);
            return Returning(service.AddOrder(email, newOrder));
        }

        private static string GetEmail(IEnumerable<Claim> given)
        {
            return given.FirstOrDefault(x => x.Type == "http://schemas.xmlsoap.org/ws/2005/05/identity/claims/name").Value;
        }

        private IActionResult Returning(object fromService)
        {
            Type type = fromService.GetType();
            if (type.Equals(typeof(OKOutput<Order>)))
                return Ok(fromService);
            if (type.Equals(typeof(OKAllOutput<Order>)))
                return Ok(fromService);
            if (type.Equals(typeof(BadRequestOutput)))
                return BadRequest(fromService);
            if (type.Equals(typeof(NotFoundOutput)))
                return NotFound(fromService);
            return BadRequest(new Dictionary<string, string> { { "status", "unknown error" } });
        }
    }
}
