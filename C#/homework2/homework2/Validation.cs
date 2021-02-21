using System;
using System.Collections.Generic;
using System.IO;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace homework1
{
    static class Validation
    {
        public static int ValidateInt(string given_input)
        {
            int toReturn;
            try
            {
                toReturn = Convert.ToInt32(given_input);
            }
            catch
            {
                throw new Exception("Input not an int");
            }
            return toReturn;
        }
        public static int ValidateId(string given_input)
        {
            int toReturn;
            try
            {
                toReturn = Convert.ToInt32(given_input);
            }
            catch
            {
                throw new Exception("Id not an int");
            }
            if (toReturn <= 0)
            {
                throw new Exception("Id has to be larger than 0");
            }
            return toReturn;
        }

        public static double ValidatePrice(string given_input)
        {
            double toReturn;
            try
            {
                toReturn = double.Parse(given_input, System.Globalization.CultureInfo.InvariantCulture);
            }
            catch
            {
                throw new Exception("Price not a number");
            }
            if (toReturn < 0)
            {
                throw new Exception("Price is lower than 0");
            }
            toReturn = Math.Round(toReturn, 2);
            return toReturn;
        }
        public static double ValidateDuration(string given_input)
        {
            double toReturn;
            try
            {
               toReturn = double.Parse(given_input, System.Globalization.CultureInfo.InvariantCulture);
            }
            catch
            {
                throw new Exception("Duration not a number");
            }
            if (toReturn <= 0)
            {
                throw new Exception("Duration has to be positive");
            }
            toReturn = Math.Round(toReturn, 1);
            return toReturn;
        }
        public static DateTime ValidateDateTime(string given_input)
        {
            try
            {
                DateTime toReturn = DateTime.ParseExact(given_input, "yyyy MM dd HH mm ss", System.Globalization.CultureInfo.InvariantCulture);
                return toReturn;
            }
            catch
            {
                throw new Exception("Input is not Date & Time");
            }
        }
        public static RestaurantNames ValidateRestName(string given_input)
        {
            try
            {
                int toReturn = Convert.ToInt32(given_input); ;
                if (!typeof(RestaurantNames).IsEnumDefined(toReturn))
                {
                    throw new Exception("No such restaurant");
                }
                return (RestaurantNames)toReturn;
            }
            catch (Exception e) when (e.Message != "No such restaurant")
            {
                throw new Exception("Restaurant selection is done using a number from list");
            }
        }
        public static bool ValidateFileName(string given_input)
        {
            try
            {
                StreamReader file = File.OpenText(given_input);
                file.Close();
                return true;
            }
            catch
            {
                return false;
            }
        }
    }
}
