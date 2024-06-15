import Protocol from '@/webclient/Protocol';
import SessionHandle from '@/webclient/Sessions/SessionHandle';
import User from './User';
import { defaultUsername } from '@/Constants';

/**
 * Represents a client user.
 */
export class ClientUser extends User {
     /**
      * Constructs a ClientUser instance.
      * @param username The username of the client user.
      */
     constructor(username: string) {
          super(username);
     }

     /**
      * Updates the username from the username cookie.
      * It is changeable by the user, but it should not be a big deal. Unless?
      */
     updateFromSession(): void {
          let username = SessionHandle.getCookie('username');
          if (!username) return;
          this.username.value = Protocol.Sessions.decryptUsername(username);
          if (this.username.value != defaultUsername)
               this.isGuest.value = false;
     }

     /**
      * Logs the client user in.
      */
     logIn(): void {
          this.updateFromSession();
          this.isGuest.value = false;
     }

     /**
      * Logs the client user out.
      */
     logOut(): void {
          this.username.value = defaultUsername;
          this.isGuest.value = true;
     }
}

// Export a singleton instance of ClientUser with the default username
export default new ClientUser(defaultUsername);
