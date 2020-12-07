package com.mbtroads;

import io.appium.java_client.AppiumDriver;
import io.appium.java_client.MobileElement;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

import static org.junit.Assert.assertEquals;
import static org.junit.Assert.assertTrue;

import static org.graphwalker.core.common.Objects.isNotNull;
import static org.graphwalker.core.common.Objects.isNull;
import static org.graphwalker.core.model.Edge.RuntimeEdge;
import static org.graphwalker.core.model.Vertex.RuntimeVertex;
import org.graphwalker.core.machine.ExecutionContext;
import org.graphwalker.java.annotation.AfterExecution;
import org.graphwalker.java.annotation.BeforeExecution;
import org.graphwalker.java.annotation.GraphWalker;
import org.junit.Assert;
import org.openqa.selenium.By;
import org.openqa.selenium.WebElement;
import org.openqa.selenium.support.ui.ExpectedConditions;
import org.openqa.selenium.support.ui.WebDriverWait;
import org.openqa.selenium.remote.DesiredCapabilities;

import java.io.File;
import java.net.MalformedURLException;
import java.net.URL;
import java.util.List;
import java.util.Random;
import java.util.concurrent.TimeUnit;

import io.appium.java_client.MobileBy;
import io.appium.java_client.android.AndroidDriver;
import io.appium.java_client.android.AndroidKeyCode;
import io.appium.java_client.android.AndroidElement;

@GraphWalker(value = "random(edge_coverage(100))", start = "v_Initial")
public class SomeSmallTest extends ExecutionContext implements WikipediaStart {
    public AndroidDriver<WebElement> driver;

    @BeforeExecution
    public void setup() {
        DesiredCapabilities capabilities = new DesiredCapabilities();
        capabilities.setCapability("deviceName", "OnePlus 5");
        capabilities.setCapability("udid", "94343f3e");
        capabilities.setCapability("platformName", "android");
        capabilities.setCapability("platformVersion", "10");
        capabilities.setCapability("appPackage", "org.wikipedia");
        capabilities.setCapability("appActivity", "org.wikipedia.main.MainActivity");
        capabilities.setCapability("noReset", true);
        capabilities.setCapability("automationName", "uiautomator1");
        try {
            driver = new AndroidDriver<>(new URL("http://0.0.0.0:4723/wd/hub"), capabilities);
        } catch (MalformedURLException e) {
            e.printStackTrace();
        }
        driver.manage().timeouts().implicitlyWait(10, TimeUnit.SECONDS);
    }

    @AfterExecution
    public void tearDown() {
        driver.quit();
    }

    @Override
    public void e_AddDeutsch() {
        String path = "/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.view.ViewGroup/android.widget.FrameLayout[2]/android.widget.FrameLayout/androidx.recyclerview.widget.RecyclerView/android.widget.LinearLayout[5]";
        driver.findElementByXPath(path).click();
    }

    @Override
    public void v_Start2() {
        String activity = driver.currentActivity();
        Assert.assertEquals(activity, ".onboarding.InitialOnboardingActivity");
    }

    @Override
    public void v_LanguagesPage() {
        String activity = driver.currentActivity();
        Assert.assertEquals(activity, ".settings.languages.WikipediaLanguagesActivity");
    }

    @Override
    public void e_AddLanguage() {
        String path = "/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.view.ViewGroup/android.widget.FrameLayout[2]/android.widget.FrameLayout/android.widget.LinearLayout/androidx.recyclerview.widget.RecyclerView/android.widget.LinearLayout[3]";
        driver.findElementByXPath(path).click();
        driver.manage().timeouts().implicitlyWait(5, TimeUnit.SECONDS);
    }

    @Override
    public void v_Start() {
        String activity = driver.currentActivity();
        Assert.assertEquals(activity, ".onboarding.InitialOnboardingActivity");
    }

    @Override
    public void e_PressBack() {
        driver.pressKeyCode(AndroidKeyCode.BACK);
        driver.manage().timeouts().implicitlyWait(5, TimeUnit.SECONDS);
    }

    @Override
    public void v_HomePage() {
        String activity = driver.currentActivity();
        Assert.assertEquals(activity, ".main.MainActivity");
    }

    @Override
    public void e_AddLanguagesOrChange() {
        String path = "/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.FrameLayout/androidx.viewpager.widget.ViewPager/androidx.recyclerview.widget.RecyclerView/android.widget.FrameLayout/android.view.ViewGroup/android.widget.ScrollView/android.widget.LinearLayout/android.widget.LinearLayout/android.widget.LinearLayout/android.widget.LinearLayout";
        driver.findElementByXPath(path).click();
        driver.manage().timeouts().implicitlyWait(5, TimeUnit.SECONDS);
    }


    @Override
    public void v_Languages() {
        String activity = driver.currentActivity();
        Assert.assertEquals(activity, ".language.LanguagesListActivity");
    }

    @Override
    public void v_Initial() {
        String activity = driver.currentActivity();
        Assert.assertEquals(activity, ".onboarding.InitialOnboardingActivity");
    }

    @Override
    public void v_LanguagesPage2() {
        List<WebElement> languages = driver.findElements(By.id("org.wikipedia:id/wiki_language_title"));
        for(WebElement language : languages){
            String text = language.getAttribute("text");
            if(text.equals("Deutsch")){
                Assert.assertEquals(text, "Deutsch");
                break;
            }
        }
    }

    @Override
    public void e_NewEdge() {

    }
}