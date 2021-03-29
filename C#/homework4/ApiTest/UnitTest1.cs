using EventApi.Controllers;
using Microsoft.AspNetCore.Mvc;
using Microsoft.VisualStudio.TestTools.UnitTesting;
using System;
using System.Collections.Generic;
using System.ComponentModel.DataAnnotations;
using System.Linq;
using System.Reflection;

namespace EventApi
{
    [TestClass]
    public class UnitTest1
    {
        private readonly Event[] testEvents =
            {
                new Event { Title = "Normal", RestName = (RestaurantNames)Enum.Parse(typeof(RestaurantNames), "Delice"), DateTime = Convert.ToDateTime("2020-10-14 14:30:00"), Duration = 2, Price = 100},
                new Event { Title = "Normal 2", RestName = (RestaurantNames)Enum.Parse(typeof(RestaurantNames), "EuroHotel"), DateTime = Convert.ToDateTime("2022-08-10 00:00:00"), Duration = 3, Price = 1},
                new Event { Title = "Normal 3", RestName = (RestaurantNames)Enum.Parse(typeof(RestaurantNames), "Morio"), DateTime =  Convert.ToDateTime("2021-03-15 05:50:00"), Duration = 10.2m, Price = 10.5m},
                new Event { Title = "Normal 4", RestName = (RestaurantNames)Enum.Parse(typeof(RestaurantNames), "Morio"), DateTime =  Convert.ToDateTime("2029-02-14 10:00:00"), Duration = 50, Price = 80},
                new Event { Title = "Normal 5", RestName = (RestaurantNames)Enum.Parse(typeof(RestaurantNames), "Delice"), DateTime =  Convert.ToDateTime("2011-01-01 00:00:00"), Duration = 0.1m, Price = 0}
            };
        private readonly EventsController controller = new();
        public UnitTest1()
        {
            Environment.SetEnvironmentVariable("ConString", "Host=localhost;Username=postgres;Password=12345;Database=ForUnitTests");
            Repository rep = new(new PGContext());
            rep.Execute("delete from \"Events\"");
            rep.Execute("ALTER SEQUENCE \"Events_id_seq\" RESTART WITH 1");
            rep.Save();
        }

        [TestMethod]
        public void TestValidation()
        {
            Event[] wrongEvents =
            {
                new Event { },
                new Event { Title = null, RestName = (RestaurantNames)Enum.Parse(typeof(RestaurantNames), "Delice"), DateTime = Convert.ToDateTime("2020-10-14 14:30:00"), Duration = 2, Price = 3},
                new Event { Title = "", RestName = (RestaurantNames)Enum.Parse(typeof(RestaurantNames), "Delice"), DateTime = Convert.ToDateTime("2020-10-14 14:30:00"), Duration = 2, Price = 3},
                new Event { Title = "aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa", RestName = (RestaurantNames)Enum.Parse(typeof(RestaurantNames), "Delice"), DateTime = Convert.ToDateTime("2020-10-14 14:30:00"), Duration = 2, Price = 3},
                new Event { Title = "Normal", RestName = (RestaurantNames)Enum.Parse(typeof(RestaurantNames), "Delice"), DateTime = Convert.ToDateTime("2020-10-14 14:30:00"), Duration = -5, Price = 3},
                new Event { Title = "Normal", RestName = (RestaurantNames)Enum.Parse(typeof(RestaurantNames), "Delice"), DateTime = Convert.ToDateTime("2020-10-14 14:30:00"), Duration = 0, Price = 3},
                new Event { Title = "Normal", RestName = (RestaurantNames)Enum.Parse(typeof(RestaurantNames), "Delice"), DateTime = Convert.ToDateTime("2020-10-14 14:30:00"), Duration = 0.22m, Price = 3},
                new Event { Title = "Normal", RestName = (RestaurantNames)Enum.Parse(typeof(RestaurantNames), "Delice"), DateTime = Convert.ToDateTime("2020-10-14 14:30:00"), Duration = 100, Price = 3},
                new Event { Title = "Normal", RestName = (RestaurantNames)Enum.Parse(typeof(RestaurantNames), "Delice"), DateTime = Convert.ToDateTime("2020-10-14 14:30:00"), Duration = 2, Price = -5},
                new Event { Title = "Normal", RestName = (RestaurantNames)Enum.Parse(typeof(RestaurantNames), "Delice"), DateTime = Convert.ToDateTime("2020-10-14 14:30:00"), Duration = 2, Price = 2.444m},
                new Event { Title = "Normal", RestName = (RestaurantNames)Enum.Parse(typeof(RestaurantNames), "Delice"), DateTime = Convert.ToDateTime("2020-10-14 14:30:00"), Duration = 2, Price = 1000}
            };
            string[] errors =
            {
                "Should not accept empty event",
                "Should not accept null title",
                "Should not accept whitespace title",
                "Should not accept very long title",
                "Should not accept negative duration",
                "Should not accept 0 duration",
                "Should not accept more than 1 decimal in duration",
                "Should not accept large duration",
                "Should not accept negative price",
                "Should not accept more than 2 decimal in price",
                "Should not accept large price"
            };
            for (int i = 0; i < wrongEvents.Length; i++)
            {
                var validationResults = new List<ValidationResult>();
                var ctx = new ValidationContext(wrongEvents[i], null, null);
                Validator.TryValidateObject(wrongEvents[i], ctx, validationResults, true);
                Assert.IsTrue(validationResults.Any(), errors[i]);
            }
        }

        [TestMethod]
        public void Adding()
        {
            foreach (Event x in testEvents)
            {
                var result = controller.AddEvent(x);
                Assert.IsInstanceOfType(result, typeof(OkObjectResult));
            }
        }

        [TestMethod]
        public void GettingOne()
        {
            for (int i = 1; i <= 10; i++)
                Assert.IsInstanceOfType(controller.FindEvent(i), typeof(NotFoundObjectResult));
            foreach (Event x in testEvents)
                controller.AddEvent(x);
            for (int i = 1; i <= 10; i++)
            {
                if (i <= 5)
                {
                    var result = controller.FindEvent(i);
                    Assert.IsInstanceOfType(result, typeof(OkObjectResult));
                    OKOutput resultObj = (OKOutput)((OkObjectResult)result).Value;
                    Assert.IsTrue(EqualEvents(testEvents[i - 1], resultObj.Event));
                }
                else
                    Assert.IsInstanceOfType(controller.FindEvent(i), typeof(NotFoundObjectResult));
            }

        }

        [TestMethod]
        public void DeleteTest()
        {
            for (int i = 1; i <= 10; i++)
                Assert.IsInstanceOfType(controller.DeleteEvent(i), typeof(NotFoundObjectResult));

            foreach (Event x in testEvents)
                controller.AddEvent(x);

            for (int i = 1; i <= 10; i++)
            {
                if (i <= 5)
                    Assert.IsInstanceOfType(controller.DeleteEvent(i), typeof(OkObjectResult));
                Assert.IsInstanceOfType(controller.DeleteEvent(i), typeof(NotFoundObjectResult));
            }
        }

        [TestMethod]
        public void EditEvent()
        {
            Assert.IsInstanceOfType(controller.EditEvent(1, new Event()), typeof(NotFoundObjectResult));

            controller.AddEvent(testEvents[0]);

            for (int i = 1; i < testEvents.Length; i++)
            {
                var result = controller.EditEvent(1, testEvents[i]);
                Assert.IsInstanceOfType(result, typeof(OkObjectResult));
                OKOutput resultObj = (OKOutput)((OkObjectResult)result).Value;
                Assert.IsTrue(EqualEvents(testEvents[i], resultObj.Event));
            }

        }

        [TestMethod]
        public void NullEventTest()
        {
            Assert.IsInstanceOfType(controller.AddEvent(null), typeof(BadRequestObjectResult));
            Assert.IsInstanceOfType(controller.EditEvent(1, null), typeof(BadRequestObjectResult));
        }


        [TestMethod]
        public void TestGetAll()
        {
            for (int i = 0; i < testEvents.Length; i++)
            {
                controller.AddEvent(testEvents[i]);
                var result = controller.GetEvents(null, null, null, 0, 0);
                Assert.IsInstanceOfType(result, typeof(OkObjectResult));
                OKAllOutput resultObj = (OKAllOutput)((OkObjectResult)result).Value;
                Assert.AreEqual(i + 1, resultObj.Amount);
                Assert.IsTrue(EqualEvents(testEvents[i], resultObj.Events[i]));
            }
        }

        [TestMethod]
        public void TestSearch()
        {
            for (int i = 0; i < testEvents.Length; i++)
                controller.AddEvent(testEvents[i]);

            Dictionary<string, List<Event>> keyValuePairs = new()
            {
                { "14", new List<Event> { testEvents[0], testEvents[3] } },
                { "", testEvents.ToList() },
                { "Normal", testEvents.ToList() },
                { "normal", testEvents.ToList() },
                { "Delice", new List<Event> { testEvents[0], testEvents[4] } },
                { "i", new List<Event> { testEvents[0], testEvents[2], testEvents[3], testEvents[4] } },
                { "NotFound", new List<Event> { } }
            };
            foreach (KeyValuePair<string, List<Event>> x in keyValuePairs)
            {
                var result = controller.GetEvents(x.Key, null, null, 0, 0);
                OKAllOutput resultObj = (OKAllOutput)((OkObjectResult)result).Value;
                Assert.AreEqual(x.Value.Count, resultObj.Amount);
                for (int i = 0; i < x.Value.Count; i++)
                    Assert.IsTrue(EqualEvents(x.Value[i], resultObj.Events[i]));
            }
        }
        [TestMethod]
        public void TestSort()
        {
            for (int i = 0; i < testEvents.Length; i++)
                controller.AddEvent(testEvents[i]);

            Dictionary<string, List<Event>> keyValuePairs = new()
            {
                { "Title", testEvents.ToList() },
                { "title", testEvents.ToList() },
                { "RestName", new List<Event> { testEvents[0], testEvents[4], testEvents[1], testEvents[2], testEvents[3] } },
                { "DateTime", new List<Event> { testEvents[4], testEvents[0], testEvents[2], testEvents[1], testEvents[3] } },
                { "Duration", new List<Event> { testEvents[4], testEvents[0], testEvents[1], testEvents[2], testEvents[3] } },
                { "Price", new List<Event> { testEvents[4], testEvents[1], testEvents[2], testEvents[3], testEvents[0] } }
            };

            foreach (KeyValuePair<string, List<Event>> x in keyValuePairs)
            {
                var result = controller.GetEvents(null, x.Key, null, 0, 0);
                OKAllOutput resultObj = (OKAllOutput)((OkObjectResult)result).Value;
                Assert.AreEqual(x.Value.Count, resultObj.Amount);
                for (int i = 0; i < x.Value.Count; i++)
                    Assert.IsTrue(EqualEvents(x.Value[i], resultObj.Events[i]));
            }

            foreach (KeyValuePair<string, List<Event>> x in keyValuePairs)
            {
                x.Value.Reverse();
                var result = controller.GetEvents(null, x.Key, "desc", 0, 0);
                OKAllOutput resultObj = (OKAllOutput)((OkObjectResult)result).Value;
                Assert.AreEqual(x.Value.Count, resultObj.Amount);
                for (int i = 0; i < x.Value.Count; i++)
                    Assert.IsTrue(EqualEvents(x.Value[i], resultObj.Events[i]));
            }
        }
        [TestMethod]
        public void TestOffsetLimit()
        {
            for (int i = 0; i < testEvents.Length; i++)
                controller.AddEvent(testEvents[i]);

            List<List<dynamic>> toTest = new()
            {
                new List<dynamic> { 0, 0, testEvents.ToList() },
                new List<dynamic> { -3, -3, testEvents.ToList() },
                new List<dynamic> { 0, 2, testEvents.ToList() },
                new List<dynamic> { 5, 0, testEvents.ToList() },
                new List<dynamic> { 10, -3, testEvents.ToList() },
                new List<dynamic> { 10, 0, testEvents.ToList() },
                new List<dynamic> { 2, 0, new List<Event> { testEvents[0], testEvents[1] } },
                new List<dynamic> { 2, 1, new List<Event> { testEvents[2], testEvents[3] } },
                new List<dynamic> { 2, 2, new List<Event> { testEvents[4] } },
            };
            foreach (List<dynamic> x in toTest)
            {
                var result = controller.GetEvents(null, null, null, x[0], x[1]);
                OKAllOutput resultObj = (OKAllOutput)((OkObjectResult)result).Value;
                Assert.AreEqual(x[2].Count, resultObj.Amount);
                for (int i = 0; i < x[2].Count; i++)
                    Assert.IsTrue(EqualEvents(x[2][i], resultObj.Events[i]));
            }

            toTest = new List<List<dynamic>>
            {
                new List<dynamic> { 5, 1 },
                new List<dynamic> { 4, 2 },
                new List<dynamic> { 3, 2 },
                new List<dynamic> { 2, 3 },
            };
            foreach (List<dynamic> x in toTest)
                Assert.IsInstanceOfType(controller.GetEvents(null, null, null, x[0], x[1]), typeof(NotFoundObjectResult));
        }
        [TestMethod]
        public void TestCombined()
        {
            for (int i = 0; i < testEvents.Length; i++)
                controller.AddEvent(testEvents[i]);

            List<List<dynamic>> toTest = new()
            {
                new List<dynamic> { "14", "duration", null, 1, 0, testEvents[0] },
                new List<dynamic> { "14", "duration", null, 1, 1, testEvents[3] },
                new List<dynamic> { "14", "duration", "desc", 1, 0, testEvents[3] },
                new List<dynamic> { "14", "duration", "desc", 1, 1, testEvents[0] },
            };
            foreach (List<dynamic> x in toTest)
            {
                var result = controller.GetEvents(x[0], x[1], x[2], x[3], x[4]);
                OKAllOutput resultObj = (OKAllOutput)((OkObjectResult)result).Value;
                Assert.IsTrue(EqualEvents(x[5], resultObj.Events[0]));
            }
        }

        private static bool EqualEvents(Event given, Event fromDb)
        {
            foreach (PropertyInfo x in typeof(Event).GetProperties())
            {
                if (x.Name != "Id")
                    if (!x.GetValue(given).Equals(x.GetValue(fromDb)))
                        return false;
            }
            return true;
        }
    }
}