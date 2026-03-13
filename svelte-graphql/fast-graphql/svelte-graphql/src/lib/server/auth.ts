// Somehow, Typescript is looking for this dep 
// in the root project (the workspace)
// TODO: ASK GONZA
import jwt from 'jsonwebtoken';
import { JWT_SECRET_KEY } from '$env/static/private'

export interface UserPayLoad {
  id: string
  name: string
  email: string
  rol: string
}

export function authenticateUser(token: string): boolean  {
  
  try {
    const decoded = jwt.verify(token, JWT_SECRET_KEY, {
      algorithms: ['HS256']
    }) as any;
    
    if(!decoded){
      return false
    }
    
    return true // Devuelve el objeto user del payload
    
    
  } catch {
    return false;
  }
  
}


export function getUserfromPayLoad(token: string | undefined): UserPayLoad | null {
  if (!token) return null;
  
  try {
    const decoded = jwt.verify(token, JWT_SECRET_KEY, {
      algorithms: ['HS256']
    }) as any;
    
    
    return decoded.user; // Devuelve el objeto user del payload
    
    
  } catch {
    return null;
  }
}