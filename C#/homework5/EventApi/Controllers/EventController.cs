using EventApi.Services;
using Microsoft.AspNetCore.Authorization;
using Microsoft.AspNetCore.Mvc;
using System;
using System.Collections.Generic;

namespace EventApi.Controllers
{
    [Produces("application/json")]
    [ApiController]
    [Route("[controller]")]
    public class EventsController : Controller
    {
        private readonly EventService service = new();

        /// <summary>
        /// Fetches all events / Finds specific Events using partial match / Sorts / Uses pagination
        /// </summary>
        /// <param name="toFind" example="Delice">Filters events with partial search</param> 
        /// <param name="sort_param" example="title">Sorting parameter</param> 
        /// <param name="sort_type" example="Desc"> Ascending/Descending sorting</param> 
        /// <param name="limit" example="0">Contains a page with limited amout of events</param> 
        /// <param name="offset" example="0">Page number</param> 
        /// <returns> 200 response code, success message and found Event </returns>
        /// <response code="200"> Successfully found </response>
        /// <response code="404"> Empty page because of offset and limit </response>   
        /// <response code="400"> Sort parameter does not exist / Wrong type of limit / Wrong type of offset</response> 
        [HttpGet]
        [ProducesResponseType(typeof(OKAllOutput<Event>), 200)]
        [ProducesResponseType(typeof(BadRequestOutput), 400)]
        [ProducesResponseType(typeof(NotFoundOutput), 404)]
        public IActionResult GetEvents([FromQuery(Name = "what")] string toFind, [FromQuery(Name = "sort_by")] string sort_param,
            [FromQuery(Name = "sort_type")] string sort_type, [FromQuery(Name = "limit")] int limit, [FromQuery(Name = "offset")] int offset)
        {
            return Returning(service.GetEvents(toFind, sort_param, sort_type, limit, offset));
        }
        /// <summary>
        /// Finds a specific Event by given id
        /// </summary>
        /// <param name="id" example="1">Id of event to find</param> 
        /// <returns> 200 response code, success message and found Event </returns>
        /// <response code="200"> Successfully found </response>
        /// <response code="404"> Event with this id was not found </response>   
        /// <response code="400"> Id is of wrong type </response>
        [HttpGet]
        [Route("{id}")]
        [ProducesResponseType(typeof(OKOutput<Event>), 200)]
        [ProducesResponseType(typeof(BadRequestOutput), 400)]
        [ProducesResponseType(typeof(NotFoundOutput), 404)]
        public IActionResult FindEvent(int id)
        {
            return Returning(service.GetEvent(id));
        }
        /// <summary>
        /// Creates a new Event
        /// </summary>
        /// <param name="newEvent">New event data</param> 
        /// <remarks>
        /// Sample request:
        ///
        ///     POST
        ///     {
        ///        "title": "Event1",
        ///        "restName": 0,
        ///        "dateTime": "2020-10-10 14:30:00",
        ///        "price": 20.5,
        ///        "duration": 2.5
        ///     }
        ///
        /// </remarks>
        /// <returns> 200 response code, success message and created Event </returns>
        /// <response code="200"> New Event </response>
        /// <response code="400"> Event is null / Event does not pass validation / Such id already exists</response> 
        [Authorize(Roles = "Admin")]
        [HttpPost]
        [ProducesResponseType(typeof(OKOutput<Event>), 200)]
        [ProducesResponseType(typeof(BadRequestOutput), 400)]
        public IActionResult AddEvent([FromForm] Event newEvent)
        {
            return Returning(service.CreateEvent(newEvent));
        }
        /// <summary>
        /// Deletes a specific Event by given id
        /// </summary>
        /// <param name="id" example="1">Id of event to delete</param> 
        /// <returns> 200 response code, success message and deleted Event </returns>
        /// <response code="200"> Successful deletion </response>
        /// <response code="404"> Event with this id was not found </response>   
        /// <response code="400"> Id is of wrong type </response>
        [Authorize(Roles = "Admin")]
        [HttpDelete]
        [Route("{id}")]
        [ProducesResponseType(typeof(OKOutput<Event>), 200)]
        [ProducesResponseType(typeof(BadRequestOutput), 400)]
        [ProducesResponseType(typeof(NotFoundOutput), 404)]
        public IActionResult DeleteEvent(int id)
        {
            return Returning(service.DeleteEvent(id));
        }
        /// <summary>
        /// Updates event at existing id to given Event
        /// </summary>
        /// <param name="id" example="1">Id of event to update</param>
        /// <param name="newEvent">New event data</param> 
        /// <remarks>
        /// Sample request:
        ///
        ///     Put /1
        ///     {
        ///        "title": "Event1",
        ///        "restName": 0,
        ///        "dateTime": "2020-10-10 14:30:00",
        ///        "price": 20.5,
        ///        "duration": 2.5
        ///     }
        ///
        /// </remarks>
        /// <returns> 200 response code, success message and updated Event </returns>
        /// <response code="200"> Updated event </response>
        /// <response code="400"> Event is null / Event does not pass validation / Id is of wrong type </response>  
        /// <response code="404"> Event with this id was not found </response>  
        [Authorize(Roles = "Admin")]
        [HttpPut]
        [Route("{id}")]
        [ProducesResponseType(typeof(OKOutput<Event>), 200)]
        [ProducesResponseType(typeof(BadRequestOutput), 400)]
        [ProducesResponseType(typeof(NotFoundOutput), 404)]
        public IActionResult EditEvent(int id, [FromForm] Event newEvent)
        {
            return Returning(service.EditEvent(id, newEvent));
        }

        private IActionResult Returning(object fromService)
        {
            Type type = fromService.GetType();
            if (type.Equals(typeof(OKOutput<Event>)))
                return Ok(fromService);
            if (type.Equals(typeof(OKAllOutput<Event>)))
                return Ok(fromService);
            if (type.Equals(typeof(BadRequestOutput)))
                return BadRequest(fromService);
            if (type.Equals(typeof(NotFoundOutput)))
                return NotFound(fromService);
            return BadRequest(new Dictionary<string, string> { { "status", "unknown error" } });
        }
    }
}
