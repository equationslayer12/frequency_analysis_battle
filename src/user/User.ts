import { ref, Ref } from 'vue';

/**
 * Represents a signed up or guest user.
 */
export default abstract class User {
     /**
      * A boolean flag indicating whether the user is a guest or signed up.
      */
     isGuest: Ref<boolean>;

     /**
      * The username of the user.
      */
     username: Ref<string>;

     /**
      * Constructs a User instance.
      * @param username The username of the user.
      */
     constructor(username: string) {
          this.isGuest = ref(true);
          this.username = ref(username);
     }
}
