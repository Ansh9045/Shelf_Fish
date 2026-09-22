import { createContext, useContext, useState, useEffect, useCallback, useMemo } from 'react'
import { getUser, login, register } from '../services/authService'
import { setUnauthorizedHandler } from '../services/api'
import { getToken, saveToken, deleteToken } from '../services/tokenStorage'

const AuthContext = createContext()

export const AuthProvider = ({ children }) => {
    const [token, setToken] = useState(null)
    const [loading, setLoading] = useState(true)
    const [user, setUser] = useState(null)

    const signOut = useCallback(async () => {
        await deleteToken()
        setToken(null)
    }, [])

    useEffect(() => {
        getToken()
            .then(async (t) => {
                setToken(t)
                if (t) setUser(await getUser())
            }).catch((e)=>{
                setToken(null)
                setUser(null)
                console.error(e)
                
            }).finally(()=> setLoading(false))
    }, [])
    useEffect(() => {
        setUnauthorizedHandler(signOut)
        return () => setUnauthorizedHandler(null)
    }, [signOut])

    const signIn = useCallback(async (username, password) => {
        const access_token = await login(username, password)
        await saveToken(access_token)
        setToken(access_token)
    }, [])
    const signUp = useCallback(async (username, email, full_name, password)=>{
        await register(username, email, full_name, password)
        await signIn(username, password)
    },[signIn])
    const value = useMemo(
        () => ({ isSignedIn: !!token, signIn,signUp, signOut, loading, user }),
        [token, signIn, signOut, loading, user]
    )
    return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>
}

export const useAuth = () => {
    const context = useContext(AuthContext)
    if (!context) {
        throw new Error('useAuth must be used within AuthProvider')
    }
    return context
}