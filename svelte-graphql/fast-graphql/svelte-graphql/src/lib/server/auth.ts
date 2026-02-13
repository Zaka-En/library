import { jwtDecode } from "jwt-decode";

export interface UserPayLoad{
  token: string;
  id: string
  name: string
  rol: string
}

export function authenticateUser(token: string | undefined): UserPayLoad | null {
  if(!token ) return null
  
  try{
    const decoded: any = jwtDecode(token)
    
    const isExpired = decoded.exp * 1000 < Date.now();
    if(isExpired) return null;

    return{
      token,
      id: decoded.sub,
      name: decoded.name,
      rol: decoded.rol
    }
  }catch(error){
    return null
  }
}