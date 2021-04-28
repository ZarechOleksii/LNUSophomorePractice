using System;
using System.ComponentModel.DataAnnotations;

namespace EventApi
{
    public class Event
    {
        [Key]
        public int Id { get; set; }
        /// <summary>
        /// Event title
        /// </summary>
        /// <example>Event1</example>
        [Required(AllowEmptyStrings = false, ErrorMessage = "Title can't be null")]
        [StringLength(30, ErrorMessage = "Title cannot be longer than 30 characters")]
        public string Title { get; set; }
        /// <summary>
        /// Event duration
        /// </summary>
        /// <example>2.5</example>
        [Required(ErrorMessage = "Duration can't be null")]
        [Range(0.1, 99.9, ErrorMessage = "Wrong Duration")]
        [RegularExpression(@"^\d+(\,\d{1,1})?$", ErrorMessage = "Maximum one decimal space for duration")]
        public decimal Duration { get; set; }
        /// <summary>
        /// Event price
        /// </summary>
        /// <example>20.5</example>
        [Required(ErrorMessage = "Price can't be null")]
        [Range(0, 999.75, ErrorMessage = "Wrong Price")]
        [RegularExpression(@"^\d+(\,\d{1,2})?$", ErrorMessage = "Maximum two decimal spaces for price")]
        public decimal Price { get; set; }
        [Required(ErrorMessage = "Restaurant name can't be null or whitspace")]
        [EnumDataType(typeof(RestaurantNames), ErrorMessage = "Not a restaurant")]
        public RestaurantNames RestName { get; set; }
        /// <summary>
        /// When Event is
        /// </summary>
        /// <example>2020-10-10 14:30:00</example>
        [Required(ErrorMessage = "Datetime cannot be null")]
        [DataType(DataType.DateTime, ErrorMessage = "Not a datetime")]
        public DateTime DateTime { get; set; }
        /// <summary>
        /// Event in stock
        /// </summary>
        /// <example>10</example>
        [Required(ErrorMessage = "Amount cannot be null")]
        [Range(0, 1000, ErrorMessage = "Wrong Amount")]
        public int Amount { get; set; }

    }
}
