using System;
using System.Collections.Generic;
using System.ComponentModel.DataAnnotations;
using System.Linq;
using System.Threading.Tasks;

namespace EventApi
{
    public class Person
    {
        [Key]
        [Required(AllowEmptyStrings = false, ErrorMessage = "No email")]
        [DataType(DataType.EmailAddress, ErrorMessage = "Not an email")]
        [StringLength(320, ErrorMessage = "Email too long")]
        public string Email { get; set; }

        public string Password { get; set; }

        [EnumDataType(typeof(Roles))]
        public Roles Role { get; set; }
    }
}
