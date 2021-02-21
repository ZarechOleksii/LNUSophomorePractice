﻿using System;
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
            string[] properties = new string[] {"Id", "Title","Price", "Duration", "DateTime", "RestName" };
            foreach (string x in properties)
            {
                to_return += x + " - " + typeof(Event).GetProperty(x).GetValue(this) + "\n"; 
            }
            return to_return;
        }
        public bool Correct()
        {
            return !errors.Any();
        }
        //setters & getters
        public dynamic Id
        {
            get { return this.id; }
            set 
            {
                int new_id_int = Validation.ValidateId(value);
                this.id = new_id_int;
            }
        }
        public dynamic Title
        {
            get { return this.title; }
            set { this.title = value; }
        }
        public dynamic Price
        {
            get { return this.price; }
            set
            {
                double new_price_double = Validation.ValidatePrice(value);
                this.price = new_price_double;
            }
        }
        public dynamic Duration
        {
            get { return this.duration; }
            set
            {
                double new_duration_double = Validation.ValidateDuration(value);
                this.duration = new_duration_double;
            }
        }

        public dynamic DateTime
        {
            get { return this.dateAndTime; }
            set
            {
                DateTime new_datetime = Validation.ValidateDateTime(value);
                this.dateAndTime = new_datetime;
            }
        }
        public dynamic RestName
        {
            get { return this.restName; }
            set
            {
                RestaurantNames new_rest_name = Validation.ValidateRestName(value);
                this.restName = new_rest_name;
            }
        }
    }
}
