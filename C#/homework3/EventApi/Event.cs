using Microsoft.EntityFrameworkCore;
using Microsoft.OpenApi.Validations;
using System;
using System.Collections.Generic;
using System.ComponentModel.DataAnnotations;
using System.Globalization;
using System.Linq;
using System.Reflection;
using System.Text;
using System.Threading.Tasks;

namespace EventApi
{
    public class Event
    {
        [Key]
        public int Id { get; set; }

        [Required(AllowEmptyStrings = false, ErrorMessage = "Title can't be null")]
        [StringLength(30, ErrorMessage = "Title cannot be longer than 30 characters")]
        public string Title { get; set; }

        [Required(ErrorMessage = "Duration can't be null")]
        [Range(0.1, 99.9, ErrorMessage = "Wrong Duration")]
        [RegularExpression(@"^\d+(\,\d{1,1})?$", ErrorMessage = "Maximum one decimal space for duration")]
        public decimal Duration { get; set; }

        [Required(ErrorMessage = "Price can't be null")]
        [Range(0, 999.75, ErrorMessage = "Wrong Price")]
        [RegularExpression(@"^\d+(\,\d{1,2})?$", ErrorMessage = "Maximum two decimal spaces for price")]
        public decimal Price { get; set; }

        [Required(ErrorMessage = "Restaurant name can't be null or whitspace")]
        [EnumDataType(typeof(RestaurantNames), ErrorMessage = "Not a restaurant")]
        public RestaurantNames RestName { get; set; }

        [Required(ErrorMessage = "Datetime cannot be null")]
        [DataType(DataType.DateTime, ErrorMessage = "Not a datetime")]
        public DateTime DateTime { get; set; }
        
    }
}
