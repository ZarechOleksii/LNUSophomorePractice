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
    public class Event : IValidatableObject
    {
        public string Title { get; set; }
        public double Duration { get; set; }
        public double Price { get; set; }
        public string RestName { get; set; }
        public string DateTime { get; set; }
        
        public IEnumerable<ValidationResult> Validate(ValidationContext validationContext)
        {
            List<ValidationResult> errors = new();
            if (string.IsNullOrWhiteSpace(this.Title))
                errors.Add(new ValidationResult("No title"));
            else if (this.Title.Length > 30)
                errors.Add(new ValidationResult("Title too long"));
            if (this.Duration <= 0 || this.Duration >= 100)
                errors.Add(new ValidationResult("Wrong duration"));
            if (this.Price < 0 || this.Price >= 1000)
                errors.Add(new ValidationResult("Wrong Price"));
            if (string.IsNullOrWhiteSpace(this.RestName))
                errors.Add(new ValidationResult("No restaurant name"));
            else if (!Enum.IsDefined(typeof(RestaurantNames), this.RestName))
                errors.Add(new ValidationResult("No such restaurant"));
            if (!System.DateTime.TryParse(this.DateTime, out _))
                errors.Add(new ValidationResult("Wrong datetime"));
            return errors;
        }
    }
}
