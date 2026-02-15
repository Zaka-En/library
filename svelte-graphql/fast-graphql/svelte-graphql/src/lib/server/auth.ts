import jwt from 'jsonwebtoken';
import { JWT_SECRET_KEY } from '$env/static/private'

export interface UserPayLoad {
  //id: string
  name: string
  email: string
  rol: string
}

export function authenticateUser(token: string | undefined): UserPayLoad | null {
  if (!token) return null;
  
  try {
    const decoded = jwt.verify(token, JWT_SECRET_KEY, {
      algorithms: ['HS256']
    }) as any;
    
    
    if (decoded.refresh) return null;
    
    return decoded.user; // Devuelve el objeto user del payload
  } catch {
    return null;
  }
}