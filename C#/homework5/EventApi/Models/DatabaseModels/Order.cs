using System;
using System.Collections.Generic;
using System.ComponentModel.DataAnnotations;
using System.ComponentModel.DataAnnotations.Schema;
using System.Linq;
using System.Threading.Tasks;

namespace EventApi
{
    public class Order
    {
        [Key]
        public int Id { get; set; }

        [Required]
        [ForeignKey("Event_Id")]
        public Event Event { get; set; }
        public int Event_Id { get; set; }

        [ForeignKey("Person_Email")]
        public Person Person { get; set; }
        public string Person_Email { get; set; }
        /// <summary>
        /// Datetime of order
        /// </summary>
        /// <example>10</example>
        public DateTime DateTime { get; set; }
        /// <summary>
        /// How much to order
        /// </summary>
        /// <example>10</example>
        [Required(ErrorMessage = "Amount cannot be null")]
        [Range(0, 1000, ErrorMessage = "Wrong Amount")]
        public int Amount { get; set; }
    }
}
