using Microsoft.AspNetCore.Mvc;
using System;
using System.Collections.Generic;
using System.Linq;
using System.Security.Claims;
using System.Text;
using System.Security.Cryptography;
using Microsoft.AspNetCore.Cryptography.KeyDerivation;
using System.Threading.Tasks;
using System.IdentityModel.Tokens.Jwt;
using Microsoft.IdentityModel.Tokens;

namespace EventApi.Services
{
    public class UserService : IUserService
    {
        private readonly Repository<Person> rep = new(new PGContext());

        public object Register(RequestModels.RegisterModel data)
        {
            if (data == null)
                return new BadRequestOutput() { Message = "data is null", Status = 400 };
            if (rep.Present(new object[] { data.Email }))
                return new BadRequestOutput() { Message = "email already registered", Status = 400 };
            Person toAdd = new() { Email = data.Email, Password = HashPassword(data.Password), Role = Roles.User };
            rep.Add(toAdd);
            rep.Save();
            string token = GetToken(NewIdentity(data.Email));
            return new TokenOutput() { Status = 200, Message = "Success", Email = data.Email, Token = token };
        }
        public object Login(RequestModels.LoginModel data)
        {
            if (data == null)
                return new BadRequestOutput() { Message = "data is null", Status = 400 };
            Person user = rep.GetT(new object[] { data.Email });
            if (user == null)
                return new BadRequestOutput() { Message = "user with such email does not exist", Status = 404 };
            if (!CheckPassword(user.Password, data.Password))
                return new BadRequestOutput() { Message = "Wrong password", Status = 400 };

            string token = GetToken(GetIdentity(user));
            return new TokenOutput() { Status = 200, Message = "Success", Email = data.Email, Token = token };
        }
        private static ClaimsIdentity NewIdentity(string email)
        {
            var claims = new List<Claim>
            {
                new Claim(ClaimsIdentity.DefaultNameClaimType, email),
                new Claim(ClaimsIdentity.DefaultRoleClaimType, Roles.User.ToString())
            };
            ClaimsIdentity claimsIdentity = new (claims, "Token", ClaimsIdentity.DefaultNameClaimType, ClaimsIdentity.DefaultRoleClaimType);
            return claimsIdentity;
        }
        private static ClaimsIdentity GetIdentity(Person user)
        {  
            var claims = new List<Claim>
            {
                new Claim(ClaimsIdentity.DefaultNameClaimType, user.Email),
                new Claim(ClaimsIdentity.DefaultRoleClaimType, user.Role.ToString())
            };
            ClaimsIdentity claimsIdentity = new (claims, "Token", ClaimsIdentity.DefaultNameClaimType, ClaimsIdentity.DefaultRoleClaimType);
            return claimsIdentity;
        }
        private static string GetToken(ClaimsIdentity identity)
        {
            var now = DateTime.UtcNow;
            var jwt = new JwtSecurityToken(
                    issuer: AuthOptions.ISSUER,
                    audience: AuthOptions.AUDIENCE,
                    notBefore: now,
                    claims: identity.Claims,
                    expires: now.Add(TimeSpan.FromMinutes(AuthOptions.LIFETIME)),
                    signingCredentials: new SigningCredentials(AuthOptions.GetSymmetricSecurityKey(), SecurityAlgorithms.HmacSha256));
            var encodedJwt = new JwtSecurityTokenHandler().WriteToken(jwt);
            return encodedJwt;
        }
        private static string HashPassword(string password)
        {
            byte[] salt = new byte[16];
            using (var rng = RandomNumberGenerator.Create())
            {
                rng.GetBytes(salt);
            }
            byte[] hashed = KeyDerivation.Pbkdf2(password, salt, KeyDerivationPrf.HMACSHA256, 10000, 32);
            byte[] result = new byte[48];
            salt.CopyTo(result, 0);
            hashed.CopyTo(result, 16);
            Console.WriteLine();
            return Encoding.Unicode.GetString(result);
        }

        private static bool CheckPassword(string passwordFromBase, string givenPassword)
        {
            byte[] bytes = Encoding.Unicode.GetBytes(passwordFromBase);
            byte[] salt = bytes.Take(16).ToArray();
            byte[] inBase = bytes.Skip(16).ToArray();
            byte[] hashed = KeyDerivation.Pbkdf2(givenPassword, salt, KeyDerivationPrf.HMACSHA256, 10000, 32);
            return ByteArrEqual(hashed, inBase);
        }
        private static bool ByteArrEqual(byte[] arr1, byte[] arr2)
        {
            if (arr1.Length != arr2.Length)
                return false;
            for (int i = 0; i < arr1.Length; i++)
                if (arr1[i] != arr2[i])
                    return false;
            return true;
        }
    }
}
