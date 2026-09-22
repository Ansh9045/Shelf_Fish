import { View, Text, Alert, Pressable, TextInput } from 'react-native'
import React, { useState } from 'react'
import { useAuth } from "../contexts/AuthContext"
import { useNavigation } from '@react-navigation/native'

const Login = () => {
    const { signIn } = useAuth()
    const [username, setUsername] = useState('')
    const [password, setPassword] = useState('')
    const [submitting, setSubmitting] = useState(false)
    const navigation = useNavigation()

    const handleLogin = async () => {
        if (!username.trim() || !password.trim || submitting) {
            return
        }
        try {
            setSubmitting(true)
            await signIn(username, password)

        } catch (error) {
            const status = error.response?.status
            const msg = status === 400 || status === 401 ? "Invalid username or email" : "Could not reach the server, try again."
            Alert.alert('Login failed', msg)
        } finally {
            setSubmitting(false)
        }
    }

    return (
        <View className="flex-1 items-center justify-center bg-red-600">
            <View className="w-[90%] h-[70%] rounded-lg items-center  bg-white">
                <Text className="text-red-800 mt-20 mb-10 font-extrabold text-6xl">Login</Text>
                <TextInput 
                    placeholder='username'
                    autoCapitalize='none'
                    value={username}
                    onChangeText={setUsername}
                    className="border border-gray-300 w-[80%] placeholder:text-red-600
                    text-2xl rounded-full px-6 p-2 mb-4"
                />
                <TextInput 
                    placeholder='password'
                    autoCapitalize='none'
                    autoComplete='current-password'
                    secureTextEntry
                    value={password}
                    onChangeText={setPassword}
                    onSubmitEditing={handleLogin}
                    className="border border-gray-300 w-[80%] placeholder:text-red-600
                    text-2xl rounded-full px-6 p-2 mb-4"
                />
                <Pressable onPress={handleLogin} disabled={submitting} className="bg-red-600 px-4 py-2 rounded-md mt-4">
                    <Text className="text-xl text-white font-bold">{submitting ? "Logging in....":"Login"}</Text>
                </Pressable>
                <Pressable onPress={()=>navigation.navigate('Register')}>
                    <Text>Don't have an account? Sign Up</Text>
                </Pressable>
            </View>



        </View>
    )
}

export default Login