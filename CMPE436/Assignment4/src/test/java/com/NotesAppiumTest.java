package com;

import io.appium.java_client.android.AndroidDriver;
import org.junit.*;
import org.junit.runner.RunWith;
import org.junit.runners.Parameterized;
import org.junit.runners.Parameterized.Parameters;
import org.openqa.selenium.OutputType;
import org.openqa.selenium.TakesScreenshot;
import org.openqa.selenium.WebElement;
import org.openqa.selenium.remote.DesiredCapabilities;
import org.openqa.selenium.support.ui.ExpectedConditions;
import org.openqa.selenium.support.ui.WebDriverWait;

import javax.imageio.ImageIO;
import java.awt.image.BufferedImage;
import java.io.File;
import java.io.IOException;
import java.net.MalformedURLException;
import java.net.URL;
import java.util.ArrayList;
import java.util.concurrent.TimeUnit;
import java.util.List;

public class NotesAppiumTest{
    private AndroidDriver<WebElement> driver;
    @Before
    public void setUp() throws Exception {
        DesiredCapabilities capabilities = new DesiredCapabilities();
        capabilities.setCapability("deviceName", "OnePlus 5");
        capabilities.setCapability("udid", "94343f3e");
        capabilities.setCapability("platformName", "android");
        capabilities.setCapability("platformVersion", "10");
        capabilities.setCapability("appPackage", "org.secuso.privacyfriendlynotes");
        capabilities.setCapability("appActivity", "org.secuso.privacyfriendlynotes.SplashActivity");
        capabilities.setCapability("noReset", true);
        capabilities.setCapability("automationName", "uiautomator1");
        try {
            driver = new AndroidDriver<>(new URL("http://0.0.0.0:4723/wd/hub"), capabilities);
        } catch (MalformedURLException e) {
            e.printStackTrace();
        }
        driver.manage().timeouts().implicitlyWait(10, TimeUnit.SECONDS);
    }

    @Test
    public void manageCategoriesActivityTest() throws InterruptedException {
        String path = "//android.widget.ImageButton[@content-desc=\"Open navigation drawer\"]";
        WebElement webelement = (WebElement) driver.findElementByXPath(path);
        WebDriverWait wait = new WebDriverWait(driver, 5);
        wait.until(ExpectedConditions.visibilityOf(webelement));
        webelement.click();
        String className = "android.support.v7.widget.LinearLayoutCompat";
        List<WebElement> classElements = (List<WebElement>) driver.findElementsByClassName(className);
        int count = 0;
        for(WebElement e : classElements){
            if(count == 1) e.click();
            count++;
        }
        String activity = driver.currentActivity();
        Assert.assertEquals(activity, ".ManageCategoriesActivity");
    }

    @Test
    public void textNoteactivityTest() throws InterruptedException {
        String id = "org.secuso.privacyfriendlynotes:id/fab_expand_menu_button";
        WebElement webelement = (WebElement) driver.findElementById(id);
        WebDriverWait wait = new WebDriverWait(driver, 5);
        wait.until(ExpectedConditions.visibilityOf(webelement));
        webelement.click();

        id = "org.secuso.privacyfriendlynotes:id/fab_text";
        webelement = (WebElement) driver.findElementById(id);
        wait = new WebDriverWait(driver, 5);
        wait.until(ExpectedConditions.visibilityOf(webelement));
        webelement.click();

        String activity = driver.currentActivity();
        Assert.assertEquals(activity, ".TextNoteActivity");

        id = "org.secuso.privacyfriendlynotes:id/text1";
        webelement = (WebElement) driver.findElementById(id);
        wait = new WebDriverWait(driver, 5);
        wait.until(ExpectedConditions.visibilityOf(webelement));
        String control = webelement.getAttribute("text");

        Assert.assertEquals("Default", control);
    }

    /*
    *
    * REFERENCES: https://discuss.appium.io/t/how-do-you-get-the-background-color-of-an-element-with-appium-webdriver/8384
    *
    * */

    @Test
    public void sketchNoteActivityTest() throws InterruptedException, IOException {
        String id = "org.secuso.privacyfriendlynotes:id/fab_expand_menu_button";
        WebElement webelement = (WebElement) driver.findElementById(id);
        WebDriverWait wait = new WebDriverWait(driver, 5);
        wait.until(ExpectedConditions.visibilityOf(webelement));
        webelement.click();

        id = "org.secuso.privacyfriendlynotes:id/fab_sketch";
        webelement = (WebElement) driver.findElementById(id);
        wait = new WebDriverWait(driver, 5);
        wait.until(ExpectedConditions.visibilityOf(webelement));
        webelement.click();

        String activity = driver.currentActivity();
        Assert.assertEquals(activity, ".SketchActivity");

        id = "org.secuso.privacyfriendlynotes:id/btn_color_selector";
        webelement = (WebElement) driver.findElementById(id);
        wait = new WebDriverWait(driver, 5);
        wait.until(ExpectedConditions.visibilityOf(webelement));

        org.openqa.selenium.Point point = webelement.getLocation();
        int centerX = point.getX();
        int centerY = point.getY();
        File scrFile = ((TakesScreenshot)driver).getScreenshotAs(OutputType.FILE);
        BufferedImage image = ImageIO.read(scrFile);
        int clr =  image.getRGB(centerX,centerY);

        webelement.click();

        String className = "android.widget.Button";
        List<WebElement> classElements = (List<WebElement>) driver.findElementsByClassName(className);
        classElements.get(0).click();

        id = "org.secuso.privacyfriendlynotes:id/btn_color_selector";
        webelement = (WebElement) driver.findElementById(id);
        wait = new WebDriverWait(driver, 5);
        wait.until(ExpectedConditions.visibilityOf(webelement));
        webelement.click();

        List<Integer> elementColor = new ArrayList<>();
        className = "android.widget.Button";
        classElements = (List<WebElement>) driver.findElementsByClassName(className);
        for(WebElement e : classElements){
            point = e.getLocation();
            centerX = point.getX();
            centerY = point.getY();
            scrFile = ((TakesScreenshot)driver).getScreenshotAs(OutputType.FILE);
            image = ImageIO.read(scrFile);
            int clrTemp =  image.getRGB(centerX,centerY);
            elementColor.add(clrTemp);
        }
        Assert.assertFalse(elementColor.contains(clr));

    }
}
