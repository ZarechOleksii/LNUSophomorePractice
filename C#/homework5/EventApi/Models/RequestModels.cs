using System;
using System.Collections.Generic;
using System.ComponentModel.DataAnnotations;
using System.ComponentModel.DataAnnotations.Schema;
using System.Linq;
using System.Threading.Tasks;

namespace EventApi
{
    public class RequestModels
    {
        public class BaseUserModel
        {
            [Required(AllowEmptyStrings = false, ErrorMessage = "No email")]
            [RegularExpression("^\\w+@[a-zA-Z_]+?\\.[a-zA-Z]{2,4}$", ErrorMessage = "Not an email")]
            [StringLength(320, ErrorMessage = "Email too long")]
            public string Email { get; set; }
        }
        public class LoginModel : BaseUserModel
        {
            [Required(AllowEmptyStrings = false, ErrorMessage = "No password")]
            [StringLength(100, ErrorMessage = "Password too long")]
            public string Password { get; set; }
        }
        public class RegisterModel : BaseUserModel
        {
            [Required(AllowEmptyStrings = false, ErrorMessage = "No password")]
            [RegularExpression("^(?=.*[a-z])(?=.*[A-Z])(?=.*\\d)[a-zA-Z\\d]{8,}$", ErrorMessage = "Password is too simple")]
            [StringLength(100, ErrorMessage = "Password too long")]
            public string Password { get; set; }
        }
        public class NewOrder
        {
            [Required]
            public int Event_Id { get; set; }

            [Required(ErrorMessage = "Amount cannot be null")]
            [Range(1, 1000, ErrorMessage = "Wrong Amount")]
            public int Amount { get; set; }
        }
    }
}
