/**
 * Utility class for handling session-related operations.
 */
export default class SessionHandle {
     /**
      * Retrieves the value of a cookie by its name.
      * @param cookieName The name of the cookie to retrieve.
      * @returns The value of the cookie, or undefined if the cookie is not found.
      */
     static getCookie(cookieName: string): string | undefined {
          // Get the entire cookie string
          const value = `; ${document.cookie}`;
          // Split the cookie string into parts based on the provided cookie name
          const parts = value.split(`; ${cookieName}=`);
          // If the parts array contains two elements, extract the cookie value
          if (parts.length === 2) {
               return parts.pop()?.split(';').shift();
          }
     }
}
