import { api } from './api'

export const login = async (username, password) => {
    const body = `username=${encodeURIComponent(username)}&password=${encodeURIComponent(password)}`
    const response = await api.post('/auth/login', body, {
        headers: { 'Content-Type': 'application/x-www-form-urlencoded' }
    })
    return response.data.access_token
}

export const register = async (username, email, full_name, password) =>{
    const response = await api.post('/auth/register', {
        username, email, full_name, password
    })
    return response.data
}
export const getUser = async ()=>{
    const response = await api.get('/users/me')
    return response.data
}