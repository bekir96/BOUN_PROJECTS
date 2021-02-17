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

public class ChessWalkAppiumTest{
    private AndroidDriver<WebElement> driver;
    @Before
    public void setUp() throws Exception {
        DesiredCapabilities capabilities = new DesiredCapabilities();
        capabilities.setCapability("deviceName", "OnePlus 5");
        capabilities.setCapability("udid", "94343f3e");
        capabilities.setCapability("platformName", "android");
        capabilities.setCapability("platformVersion", "10");
        capabilities.setCapability("appPackage", "cz.hejl.chesswalk");
        capabilities.setCapability("appActivity", "cz.hejl.chesswalk.MainActivity");
        capabilities.setCapability("noReset", true);
        capabilities.setCapability("automationName", "uiautomator1");
        capabilities.setCapability("unicodeKeyboard", "true");
        capabilities.setCapability("resetKeyboard", "true");
        try {
            driver = new AndroidDriver<>(new URL("http://0.0.0.0:4723/wd/hub"), capabilities);
        } catch (MalformedURLException e) {
            e.printStackTrace();
        }
        driver.manage().timeouts().implicitlyWait(10, TimeUnit.SECONDS);
    }

    @Test
    public void gameTest() throws InterruptedException {
        String id = "cz.hejl.chesswalk:id/btPlayOffline";
        WebElement webelement = (WebElement) driver.findElementById(id);
        WebDriverWait wait = new WebDriverWait(driver, 5);
        wait.until(ExpectedConditions.visibilityOf(webelement));
        webelement.click();

        String activity = driver.currentActivity();
        Assert.assertEquals(".OfflineGame", activity);

        id = "cz.hejl.chesswalk:id/btNewGame";
        webelement = (WebElement) driver.findElementById(id);
        wait = new WebDriverWait(driver, 5);
        wait.until(ExpectedConditions.visibilityOf(webelement));
        webelement.click();

        activity = driver.currentActivity();
        Assert.assertEquals(".NewGame", activity);
    }

}
