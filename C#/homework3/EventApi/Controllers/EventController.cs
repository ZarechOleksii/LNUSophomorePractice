using Microsoft.AspNetCore.Mvc;
using Npgsql;
using System;
using System.Collections.Generic;
using System.ComponentModel.DataAnnotations;
using System.Globalization;
using System.Linq;
using System.Reflection;
using System.Threading.Tasks;
using EventApi.Services;
using Microsoft.EntityFrameworkCore;
using Microsoft.AspNetCore.Mvc.ModelBinding;
using Microsoft.AspNetCore.Http;

namespace EventApi.Controllers
{
    [ApiController]
    [Route("[controller]")]
    public class EventsController : Controller
    {
        private readonly EventService service = new();

        [HttpGet]
        public IActionResult GetEvents([FromQuery(Name = "what")] string toFind, [FromQuery(Name = "sort_by")] string sort_param,
            [FromQuery(Name = "sort_type")] string sort_type, [FromQuery(Name = "limit")] int limit, [FromQuery(Name = "offset")] int offset)
        {
            return Returning(service.GetEvents(toFind, sort_param, sort_type, limit, offset));
        }

        [HttpGet]
        [Route("{id}")]
        public IActionResult FindEvent(int id)
        {
            return Returning(service.GetEvent(id));
        }

        [HttpPost]
        public IActionResult AddEvent([FromForm]Event newEvent)
        {
            return Returning(service.CreateEvent(newEvent));
        } 
        [HttpDelete]
        [Route("{id}")]
        public IActionResult DeleteEvent(int id)
        {
            return Returning(service.DeleteEvent(id));
        }

        [HttpPut]
        [Route("{id}")]
        public IActionResult EditEvent(int id, [FromForm]Event newEvent)
        {
            return Returning(service.EditEvent(id, newEvent));
        }

        private IActionResult Returning(Dictionary<string, dynamic> dict)
        {
            switch (dict["status"])
            {
                case 200: return Ok(dict);
                case 400: return BadRequest(dict);
                case 404: return NotFound(dict);
                case 403: return Unauthorized(dict);
                default: return BadRequest(new Dictionary<string, string> {{ "status", "unknown error" }});
            }
        }
    }
}
