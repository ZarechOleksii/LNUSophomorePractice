using System;
using System.Collections.Generic;
using System.Linq;
using System.Reflection;
using System.Text;
using System.Threading.Tasks;

namespace homework1
{
    public class Event
    {
        private int id;
        private string title;
        private double duration;
        private double price;
        private RestaurantNames restName;
        private DateTime dateAndTime;
        private List<string> errors = new List<string> { };

        public Event(){ }
        public Event(Dictionary<string, string> givDict)
        {
            foreach (KeyValuePair<string, string> x in givDict)
            {
                try
                {
                    this.GetType().GetProperty(x.Key).SetValue(this, x.Value);
                }
                catch (Exception e)
                {
                    errors.Add(e.InnerException.Message);
                }
            }
        }
        public void PrintErrors()
        {
            foreach (string x in this.errors)
            {
                Console.WriteLine($"{x}");
            }
        }
        override public string ToString()
        {
            string to_return = "";
            foreach (PropertyInfo x in this.GetType().GetProperties())
            {
                to_return += x.Name + " - " + x.GetValue(this) + "\n"; 
            }
            return to_return;
        }
        public bool Correct()
        {
            return !errors.Any();
        }
        //setters & getters
        public int Id
        {
            get { return this.id; }
            set { this.id = Validation.ValidateId(value); }
        }
        public string Title
        {
            get { return this.title; }
            set { this.title = value; }
        }
        public double Price
        {
            get { return this.price; }
            set { this.price = Validation.ValidatePrice(value); }
        }
        public double Duration
        {
            get { return this.duration; }
            set { this.duration = Validation.ValidateDuration(value); }
        }

        public DateTime DateTime
        {
            get { return this.dateAndTime; }
            set{ this.dateAndTime = value; }
        }
        public dynamic RestName
        {
            get { return this.restName; }
            set { this.restName = Validation.ValidateRestName(value); }
        }
    }
}
