import {
     MAX_PASSWORD_LENGTH,
     MAX_USERNAME_LENGTH,
     MIN_PASSWORD_LENGTH,
     MIN_USERNAME_LENGTH,
} from '@/Constants';

/**
 * Regular expression for validating alphanumeric characters.
 */
const alphaNumericRegex = /^[a-zA-Z0-9\s]+$/;

/**
 * Regular expression for validating passwords.
 */
const passwordRegex = /^[a-zA-Z0-9!@#$%^&*()-=_+\s]+$/;

/**
 * Regular expression for validating email addresses.
 */
const emailRegex =
     /^(([^<>()\[\]\\.,:\s@"]+(\.[^<>()\[\]\\.,:\s@"]+)*)|(".+"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$/;

/**
 * Validates a username.
 * @param username The username to validate.
 * @returns True if the username is valid, otherwise false.
 */
export function validateUsername(username: string): boolean {
     // min <= username.length <= max
     if (
          !(
               MIN_USERNAME_LENGTH <= username.length &&
               username.length <= MAX_USERNAME_LENGTH
          )
     ) {
          return false;
     }

     return alphaNumericRegex.test(username);
}

/**
 * Validates a password.
 * @param password The password to validate.
 * @returns True if the password is valid, otherwise false.
 */
export function validatePassword(password: string): boolean {
     // min <= password.length <= max
     if (
          !(
               MIN_PASSWORD_LENGTH <= password.length &&
               password.length <= MAX_PASSWORD_LENGTH
          )
     ) {
          return false;
     }

     return passwordRegex.test(password);
}

/**
 * Validates an email address.
 * @param email The email address to validate.
 * @returns True if the email address is valid, otherwise false.
 */
export function validateEmail(email: string): boolean {
     return emailRegex.test(email);
}
