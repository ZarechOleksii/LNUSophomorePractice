using Microsoft.IdentityModel.Tokens;
using System.Text;


namespace EventApi
{
    public class AuthOptions
    {
        public const string ISSUER = "MyAuthServer";
        public const string AUDIENCE = "MyAuthClient";
        const string KEY = "My secret key is ABOBA. Awesome. Spectacular. Truly Wonderful.";
        public const int LIFETIME = 1000;
        public static SymmetricSecurityKey GetSymmetricSecurityKey()
        {
            return new SymmetricSecurityKey(Encoding.ASCII.GetBytes(KEY));
        }
    }
}
