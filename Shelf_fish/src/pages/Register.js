import { StyleSheet, Text, View, Alert, Pressable, TextInput } from 'react-native'
import React, { useEffect, useState } from 'react'
import { useAuth } from "../contexts/AuthContext"

const Register = () => {
  const { signUp } = useAuth()
  const [username, setUsername] = useState('')
  const [email, setEmail] = useState('')
  const [name, setName] = useState('')
  const [password, setPassword] = useState('')
  const [submitting, setSubmitting] = useState(false)
  const [password2, setPassword2] = useState('')
  const [showPassword, setShowPassword] = useState(false)
  const [error, setError] = useState('')

  const handleRegister = async () => {
    if (!username.trim() || !email.trim() || !password.trim() || !password2.trim() || !name.trim()) {
      setError("All Fields must be filled!!!")
      return
    }
    if (submitting) return
    if (!(password === password2)) {
      setError("Passwords don't match")
      return
    }
    try {
      setSubmitting(true)
      await signUp( username, email, name, password )

    } catch (err) {
      const status = err.response?.status
      const msg = status === 400 ? (err.response?.data?.detail || "Username or email already exist") : "Could not reach Server, try again"
      setError(msg)
    } finally {
      setSubmitting(false)
    }
  }
  useEffect(()=>{
    if (error){
      Alert.alert('Registration failed', error)
      setError('')
    }
  }, [error])

  return (
    <View className="flex-1 items-center justify-center bg-red-600">
      <View className="items-center bg-white rounded-lg w-[90%] h-[70%]">
        <Text className="text-red-800 mt-20 mb-10 font-extrabold text-6xl">Register</Text>
        <TextInput
          placeholder='Username'
          autoCapitalize='none'
          value={username}
          onChangeText={setUsername}
          className="border border-gray-300 w-[80%] placeholder:text-red-600 text-2xl rounded-full px-6 py-2 mb-4"
        />
        <TextInput
          placeholder='Email'
          autoCapitalize='none'
          keyboardType='email-address'
          autoComplete='email'
          value={email}
          onChangeText={setEmail}
          className="border border-gray-300 w-[80%] placeholder:text-red-600 text-2xl rounded-full px-6 py-2 mb-4"
        />
        <TextInput
          placeholder='Full Name'
          autoCapitalize='words'
          value={name}
          onChangeText={setName}
          className="border border-gray-300 w-[80%] text-2xl rounded-full px-6 py-2 mb-4 placeholder:text-red-600"
        />
        <TextInput
          placeholder="Password"
          autoCapitalize='none'
          autoComplete='new-password'
          secureTextEntry
          value={password}
          onChangeText={setPassword}
          className="border border-gray-300 w-[80%] text-2xl rounded-full px-6 py-2 mb-4 placeholder:text-red-600"
        />
        <TextInput
          placeholder="Confirm Password"
          autoCapitalize='none'
          autoComplete='none'
          secureTextEntry
          value={password2}
          onChangeText={setPassword2}
          className="border border-gray-300 w-[80%] text-2xl rounded-full px-6 py-2 mb-4 placeholder:text-red-600"
        />
        <Pressable className="bg-red-600 px-4 py-2 rounded-md mt-4" onPress={handleRegister}>
          <Text className="text-xl font-bold text-white">{submitting? "Signing Up...":"Sign Up"}</Text>
        </Pressable>
      </View>
    </View>
  )
}

export default Register

const styles = StyleSheet.create({})