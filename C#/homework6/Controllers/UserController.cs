using EventApi.Services;
using Microsoft.AspNetCore.Mvc;
using System;
using System.Collections.Generic;
using System.Linq;
using System.Security.Claims;
using System.Threading.Tasks;


namespace EventApi.Controllers
{
    [Produces("application/json")]
    [ApiController]
    [Route("[controller]")]
    public class UserController : Controller
    {
        private readonly UserService service = new();

        /// <summary>
        /// Registers new user
        /// </summary>
        /// <returns> 200 response code, success message, user email and jwt token </returns>
        /// <response code="200"> Successfully registered </response>
        /// <response code="400"> Data is null / Email already registered / Wrong email format / Easy password </response>
        [ProducesResponseType(typeof(TokenOutput), 200)]
        [ProducesResponseType(typeof(BadRequestOutput), 400)]
        [HttpPost("/api/register")]
        public IActionResult Register(RequestModels.RegisterModel data)
        {
            return Returning(service.Register(data));
        }
        /// <summary>
        /// Logins into existing user
        /// </summary>
        /// <returns> 200 response code, success message, user email and jwt token </returns>
        /// <response code="200"> Successful login </response>
        /// <response code="404"> Email is not registered </response>
        /// <response code="400"> Data is null / Wrong password / Wrong email format </response>
        [ProducesResponseType(typeof(TokenOutput), 200)]
        [ProducesResponseType(typeof(NotFoundOutput), 404)]
        [ProducesResponseType(typeof(BadRequestOutput), 400)]
        [HttpPost("/api/login")]
        public IActionResult Login(RequestModels.LoginModel data)
        {
            return Returning(service.Login(data));
        }

        private IActionResult Returning(object fromService)
        {
            Type type = fromService.GetType();
            if (type.Equals(typeof(OKOutput<Person>)) || type.Equals(typeof(TokenOutput)))
                return Ok(fromService);
            if (type.Equals(typeof(OKAllOutput<Person>)))
                return Ok(fromService);
            if (type.Equals(typeof(BadRequestOutput)))
                return BadRequest(fromService);
            if (type.Equals(typeof(NotFoundOutput)))
                return NotFound(fromService);
            return BadRequest(new Dictionary<string, string> { { "status", "unknown error" } });
        }
    }
}
