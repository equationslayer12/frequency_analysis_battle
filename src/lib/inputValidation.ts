import {
     MAX_PASSWORD_LENGTH,
     MAX_USERNAME_LENGTH,
     MIN_PASSWORD_LENGTH,
     MIN_USERNAME_LENGTH,
} from '@/Constants';

const alphaNumericRegex = /^[a-zA-Z0-9\s]+$/;
const passwordRegex = /^[a-zA-Z0-9!@#$%^&*()-=_+\s]+$/;
const emailRegex =
     /^(([^<>()\[\]\\.,:\s@"]+(\.[^<>()\[\]\\.,:\s@"]+)*)|(".+"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$/;
export function validateUsername(username: string): boolean {
     // min <= username.length <= max
     console.log(username.length);
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

export function validatePassword(password: string): boolean {
     // min <= password.length <= max
     console.log(password.length);
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

export function validateEmail(email: string): boolean {
     return emailRegex.test(email);
}
