import "./global.css"
import { Text, View, ActivityIndicator } from "react-native";
import CameraComponent from "./src/components/CameraComponent";
import UploadComponent from "./src/components/UploadComponent";
import Login from "./src/pages/Login";
import { AuthProvider, useAuth } from "./src/contexts/AuthContext";
import Home from "./src/pages/Home";
import { NavigationContainer, DefaultTheme } from "@react-navigation/native";
import { createNativeStackNavigator } from "@react-navigation/native-stack";
import Register from "./src/pages/Register"
import ItemCreate from "./src/pages/ItemCreate"
import { SafeAreaProvider, SafeAreaView } from "react-native-safe-area-context"
import AllItems from "./src/pages/AllItems"
import MyItems from  "./src/pages/MyItems"
import ItemDetails from "./src/pages/ItemDetails"
import Request from "./src/pages/Request"
import MyRation from "./src/pages/MyRation"


const Stack = createNativeStackNavigator()

const navTheme = {
  ...DefaultTheme,
  colors: {
    ...DefaultTheme.colors,
    background: 'transparent',
  }
}

const AppComponent = () => {
  const { isSignedIn, loading } = useAuth()

  if (loading) {
    return <View className="flex-1 items-center justify-center">
      <ActivityIndicator size="large" color="red" />
    </View>
  }
  return (
    <SafeAreaProvider>
      <View className="flex-1 bg-deep-red">

      <SafeAreaView className="flex-1">
        <NavigationContainer theme={navTheme}>
          <Stack.Navigator screenOptions={{
            headerShown: false,
            animation: 'fade',
            contentStyle: { backgroundColor: 'transparent' }
          }}>
            {isSignedIn ? (
              <>
                <Stack.Screen name="Home" component={Home}/>
                <Stack.Screen name="ItemCreate" component={ItemCreate}/>
                <Stack.Screen name="Camera" component={CameraComponent}/>
                <Stack.Screen name="Upload" component={UploadComponent}/>
                <Stack.Screen name="AllItems" component={AllItems}/>
                <Stack.Screen name="MyItems" component={MyItems}/>
                <Stack.Screen name="ItemDetails" component={ItemDetails}/>
                <Stack.Screen name="Request" component={Request}/>
                <Stack.Screen name="MyRation" component={MyRation}/>
              </>
            ) : (
              <>
                <Stack.Screen name="Login" component={Login}/>
                <Stack.Screen name="Register" component={Register}/>

              </>
            )}
          </Stack.Navigator>
        </NavigationContainer>
      </SafeAreaView>
      </View>
    </SafeAreaProvider>
  )

}

export default function App() {

  return (
    <AuthProvider>
      <AppComponent />

    </AuthProvider>
  );
}