import { Pressable, StyleSheet, Text, View } from 'react-native'
import React from 'react'
import { useAuth } from '../contexts/AuthContext'
import { useNavigation } from '@react-navigation/native'

const Home = () => {
  const { user, signOut } = useAuth()
  const navigation = useNavigation()
  return (
    <View className="items-center justify-center" style={{ flex: 1 }}>
      <Text className="text-5xl mb-4">HELLO {user?.username.toUpperCase()}</Text>
      <View className="flex-row justify-center items-center gap-4 mb-4">

        <Pressable onPress={() => { navigation.navigate('Camera') }} className="bg-amber-400 px-6 py-3 rounded-full">
          <Text className="text-xl text-red-700 font-bold">Camera</Text>
        </Pressable>

        <Pressable onPress={()=>{ navigation.navigate('Upload')}} className="bg-amber-400 px-6 py-3 rounded-full">
          <Text className="text-xl text-red-700 font-bold">Upload</Text>
        </Pressable>
      
      </View>

      <Pressable onPress={signOut} className="bg-red-700 px-6 py-3 rounded-full border-2 border-amber-400">
        <Text className="text-md text-white font-bold">Sign Out</Text>
      </Pressable>
    </View>
  )
}

export default Home

const styles = StyleSheet.create({})