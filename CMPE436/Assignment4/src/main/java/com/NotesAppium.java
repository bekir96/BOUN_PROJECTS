package com;

import java.net.MalformedURLException;
import java.net.URL;
import java.util.*;
import java.text.DecimalFormat;
import java.util.concurrent.TimeUnit;


import org.openqa.selenium.WebElement;
import org.openqa.selenium.remote.DesiredCapabilities;
import io.appium.java_client.android.AndroidDriver;
import io.appium.java_client.android.AndroidKeyCode;
import io.appium.java_client.android.AndroidElement;

/**
 * @author Bekir Yıldırım
 */
public class NotesAppium {
    public static AndroidDriver<WebElement> driver;
    public static void setup() {
        DesiredCapabilities capabilities = new DesiredCapabilities();
        capabilities.setCapability("deviceName", "OnePlus 5");
        capabilities.setCapability("udid", "94343f3e");
        capabilities.setCapability("platformName", "android");
        capabilities.setCapability("platformVersion", "10");
        capabilities.setCapability("appPackage", "org.secuso.privacyfriendlynotes");
        capabilities.setCapability("appActivity", "org.secuso.privacyfriendlynotes.ManageCategoriesActivity");
        capabilities.setCapability("noReset", true);
        capabilities.setCapability("automationName", "uiautomator1");
        try {
            driver = new AndroidDriver<>(new URL("http://0.0.0.0:4723/wd/hub"), capabilities);
        } catch (MalformedURLException e) {
            e.printStackTrace();
        }
        driver.manage().timeouts().implicitlyWait(10, TimeUnit.SECONDS);
    }
}
