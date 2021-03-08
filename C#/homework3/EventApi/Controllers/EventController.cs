using Microsoft.AspNetCore.Mvc;
using Microsoft.AspNetCore.Mvc.ViewFeatures;
using Newtonsoft.Json;
using Newtonsoft.Json.Linq;
using Npgsql;
using System;
using System.Collections.Generic;
using System.ComponentModel.DataAnnotations;
using System.Data;
using System.Globalization;
using System.Linq;
using System.Reflection;
using System.Threading.Tasks;

namespace EventApi.Controllers
{
    [ApiController]
    [Route("[controller]")]



    public class EventsController : Controller
    {
        private readonly string[] parameters = new string[] { "id", "title", "price", "duration", "dateTime", "restName" };
        [HttpGet]
        public IActionResult PrintEvents([FromQuery(Name = "what")] string toFind, [FromQuery(Name = "sort_by")] string sort_param,
            [FromQuery(Name = "sort_type")] string sort_type, [FromQuery(Name = "limit")] int limit, [FromQuery(Name = "offset")] int offset)
        {

            string sql = "Select * from \"Events\"";
            if (!(toFind is null))
            {
                sql += " where";
                foreach (string x in parameters)
                {
                    sql += $" cast(\"{x}\" as varchar) ILIKE \'%{toFind}%\'";
                    if (!x.Equals("restName"))
                        sql += " or";
                }
            }
            if (!(sort_param is null))
            {
                if (!(sort_param is null))
                {
                    if (parameters.Contains(sort_param))
                    {
                        sql += $" order by \"{sort_param}\"";
                        if (!(sort_type is null))
                            if (sort_type.ToLower().Equals("desc") || sort_type.ToLower().Equals("asc"))
                                sql += $" {sort_type}";
                            else
                                return BadRequest(new Dictionary<string, dynamic> { { "status", 400 }, { "message", "No such sort type" } });
                    }
                    else
                        return BadRequest(new Dictionary<string, dynamic> { { "status", 400 }, { "message", "No such sort parameter" } });
                }
            }
            NpgsqlDataReader rdr = DBAccess.DataReader(sql);
            List<Dictionary<string, dynamic>> toReturn = new();
            for (int i = 0; i < offset * limit; i++)
                rdr.Read();
            while (rdr.Read())
            {
                Dictionary<string, dynamic> toAdd = createDict(rdr, rdr.FieldCount);
                toReturn.Add(toAdd);
                if (toReturn.Count == limit)
                    break;
            }
            rdr.Close();
            return Ok(toReturn);
        }
        [HttpGet]
        [Route("{id}")]
        public IActionResult PrintEvent(int id)
        {
            string sql = $"Select * from \"Events\" where Id = {id}";
            NpgsqlDataReader rdr = DBAccess.DataReader(sql);
            if (rdr.Read())
            {
                Dictionary<string, dynamic> toReturn = createDict(rdr, rdr.FieldCount);
                rdr.Close();
                return Ok(toReturn);
            }
            rdr.Close();
            return NotFound(new Dictionary<string, dynamic> { { "status", 404 }, { "message", "No such id" } });
        }
        [HttpPost]
        public IActionResult AddEvent([FromForm] Event newEvent)
        {
            string sql = "INSERT INTO \"Events\" (title, price, duration, \"dateTime\", \"restName\") ";
            sql += $"Values (\'{newEvent.Title}\', {newEvent.Price}, {newEvent.Duration}, \'{newEvent.DateTime}\', \'{newEvent.RestName}\');";
            DBAccess.ExecuteQueries(sql);
            return Ok(new Dictionary<string, dynamic> { { "status", 200 }, { "message", "success" }, { "new event", newEvent } });
        }
        [HttpDelete]
        [Route("{id}")]
        public IActionResult DeleteEvent(int id)
        {
            string sql = $"Delete from \"Events\" where Id = {id}";
            DBAccess.ExecuteQueries(sql);
            return Ok(new Dictionary<string, dynamic> { { "status", 200 }, { "message", "success" } });
        }
        [HttpPut]
        [Route("{id}")]
        public IActionResult EditEvent(int id)
        {
            string sql = $"Select * from \"Events\" where Id = {id}";
            NpgsqlDataReader rdr = DBAccess.DataReader(sql);
            if (rdr.Read())
            {
                Dictionary<string, dynamic> toEdit = createDict(rdr, rdr.FieldCount);
                rdr.Close();
                Event newEvent = new Event { Title = toEdit["title"], RestName = toEdit["restName"],
                    Price = (double)toEdit["price"], DateTime = toEdit["dateTime"].ToString(), Duration = (double)toEdit["duration"] };
                Dictionary<string, dynamic> errors = new();
                foreach (string x in Request.Form.Keys)
                {
                    PropertyInfo toChange = typeof(Event).GetProperty(x, BindingFlags.IgnoreCase | BindingFlags.Public | BindingFlags.Instance);
                    if (toChange is null)
                        errors[x] = "No such property";
                    else
                    {
                        try
                        {
                            var value = Convert.ChangeType(Request.Form[x][0], toChange.PropertyType, CultureInfo.InvariantCulture);
                            toChange.SetValue(newEvent, value);
                        }
                        catch
                        {
                            errors[x] = "Wrong property type";
                        }
                    }
                }
                var revalidation = newEvent.Validate(new ValidationContext(newEvent));
                if (revalidation.Any())
                {
                    List<string> validationErrors = new();
                    foreach (ValidationResult x in revalidation)
                        validationErrors.Add(x.ErrorMessage);
                    errors["validation"] = validationErrors;
                }
                if (errors.Any())
                    return BadRequest(new Dictionary<string, dynamic> { { "status", 400 }, { "errors", errors } });
                else
                {
                    sql = $"Update \"Events\" Set \"restName\" = \'{newEvent.RestName}\', ";
                    sql += $"title = \'{newEvent.Title}\', price = {newEvent.Price}, duration = {newEvent.Duration}, \"dateTime\" = \'{newEvent.DateTime}\'";
                    sql += $" where Id = {id}";
                    DBAccess.ExecuteQueries(sql);
                    return Ok(new Dictionary<string, dynamic> { { "status", 200 }, { "event", newEvent } });
                }
            }
            else
                return NotFound(new Dictionary<string, dynamic> { { "status", 404 }, { "message", "no such event" } });
        }
        private Dictionary<string, dynamic> createDict(NpgsqlDataReader reader, int fields)
        {
            Dictionary<string, dynamic> toReturn = new();
            for (int i = 0; i < fields; i++)
            {
                toReturn[reader.GetName(i)] = reader[i];
            }
            return toReturn;
        }
    }
}
