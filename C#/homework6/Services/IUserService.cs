using System;
using System.Collections.Generic;
using System.Linq;
using System.Threading.Tasks;

namespace EventApi.Services
{
    interface IUserService
    {
        public object Register(RequestModels.RegisterModel data);
        public object Login(RequestModels.LoginModel data);

    }
}
