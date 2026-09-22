import { Pressable, StyleSheet, Text, View } from 'react-native'
import React from 'react'
import { useAuth } from '../contexts/AuthContext'

const Home = () => {
    const {user,signOut} = useAuth()
    console.log(user)
  return (
    <View className="items-center justify-center" style={{flex:1}}>
      <Text className="text-5xl">Hello {user.username}</Text>
      <Pressable onPress={signOut}>
        <Text>Sign Out</Text>
      </Pressable>
    </View>
  )
}

export default Home

const styles = StyleSheet.create({})