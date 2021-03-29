using System.Collections.Generic;

namespace EventApi
{
    public class BadRequestOutput
    {
        /// <summary>
        /// 400 Status code
        /// </summary>
        /// <example>400</example>
        public int Status { get; set; }

        /// <summary>
        /// Error message
        /// </summary>
        /// <example>wrong input</example>
        public string Message { get; set; }
    }
    public class NotFoundOutput
    {
        /// <summary>
        /// 404 status code
        /// </summary>
        /// <example>404</example>
        public int Status { get; set; }

        /// <summary>
        /// Error message
        /// </summary>
        /// <example>not found</example>
        public string Message { get; set; }
    }
    public class OKOutput
    {
        /// <summary>
        /// 200 status code
        /// </summary>
        /// <example>200</example>
        public int Status { get; set; }

        /// <summary>
        /// Success message
        /// </summary>
        /// <example>Success</example>
        public string Message { get; set; }
        public Event Event { get; set; }
    }
    public class OKAllOutput
    {
        /// <summary>
        /// 200 status code
        /// </summary>
        /// <example>200</example>
        public int Status { get; set; }
        /// <summary>
        /// Events found
        /// </summary>
        /// <example>1</example>
        public int Amount { get; set; }
        /// <summary>
        /// Success message
        /// </summary>
        /// <example>Success</example>
        public string Message { get; set; }
        public List<Event> Events { get; set; }
    }
}
