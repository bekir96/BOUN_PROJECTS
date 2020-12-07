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
public class Test3 extends ExecutionContext implements Kesfet {
    public AndroidDriver<WebElement> driver;
    public String temp_text = "";

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
    public void e_ClickMostReaden() {
        String path = "org.wikipedia:id/view_announcement_action_negative";
        driver.findElementById(path).click();
        driver.manage().timeouts().implicitlyWait(5, TimeUnit.SECONDS);

        path = "\t\n" +
                "/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.LinearLayout/android.view.ViewGroup/androidx.viewpager.widget.ViewPager/androidx.recyclerview.widget.RecyclerView/android.widget.FrameLayout/android.view.ViewGroup/android.widget.FrameLayout/androidx.recyclerview.widget.RecyclerView/android.widget.LinearLayout[2]/android.view.ViewGroup/androidx.cardview.widget.CardView/androidx.recyclerview.widget.RecyclerView/android.view.ViewGroup[1]/android.widget.TextView[1]";
        WebElement article = driver.findElement(By.xpath(path));
        temp_text = article.getAttribute("text");
        driver.manage().timeouts().implicitlyWait(5, TimeUnit.SECONDS);

        path = "\t\n" +
                "/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.LinearLayout/android.view.ViewGroup/androidx.viewpager.widget.ViewPager/androidx.recyclerview.widget.RecyclerView/android.widget.FrameLayout/android.view.ViewGroup/android.widget.FrameLayout/androidx.recyclerview.widget.RecyclerView/android.widget.LinearLayout[2]/android.view.ViewGroup/androidx.cardview.widget.CardView/androidx.recyclerview.widget.RecyclerView/android.view.ViewGroup[1]";
        driver.findElementByXPath(path).click();
        driver.manage().timeouts().implicitlyWait(5, TimeUnit.SECONDS);
    }

    @Override
    public void e_ClickSave() {
        String path = "org.wikipedia:id/article_menu_bookmark";
        driver.findElementById(path).click();
        driver.manage().timeouts().implicitlyWait(7, TimeUnit.SECONDS);
    }

    @Override
    public void v_HomePage2() {
        String activity = driver.currentActivity();
        Assert.assertEquals(activity, ".main.MainActivity");
    }

    @Override
    public void v_Start() {
        String activity = driver.currentActivity();
        Assert.assertEquals(activity, ".onboarding.InitialOnboardingActivity");
    }

    @Override
    public void v_MostReadenSave() {
        String path = "/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.FrameLayout/androidx.drawerlayout.widget.DrawerLayout/android.widget.FrameLayout/android.widget.FrameLayout[1]/android.view.ViewGroup/android.view.ViewGroup/android.webkit.WebView/android.webkit.WebView/android.view.View/android.view.View[1]/android.view.View[1]";
        WebElement element = driver.findElement(By.xpath(path));
        String text = element.getAttribute("text");
        Assert.assertEquals(text, temp_text);
    }

    @Override
    public void e_PressBack() {
        driver.pressKeyCode(AndroidKeyCode.BACK);
        driver.manage().timeouts().implicitlyWait(5, TimeUnit.SECONDS);
    }

    @Override
    public void v_Save() {
        String path = "/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.view.ViewGroup/android.view.ViewGroup/android.widget.FrameLayout/androidx.recyclerview.widget.RecyclerView/android.view.ViewGroup[2]/android.widget.TextView[1]";
        WebElement saved = driver.findElement(By.xpath(path));
        String text = saved.getAttribute("text");
        Assert.assertEquals(text, temp_text);
    }

    @Override
    public void v_HomePage() {
        String activity = driver.currentActivity();
        Assert.assertEquals(activity, ".main.MainActivity");
        driver.manage().timeouts().implicitlyWait(5, TimeUnit.SECONDS);
    }

    @Override
    public void v_Listelerim() {
        String path = "/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.LinearLayout/android.view.ViewGroup/android.widget.TextView";
        WebElement element = driver.findElement(By.xpath(path));
        String text = element.getAttribute("text");
        Assert.assertEquals(text, "Listelerim");
        driver.manage().timeouts().implicitlyWait(5, TimeUnit.SECONDS);
    }

    @Override
    public void e_ClickListelerim() {
        String path = "//android.widget.FrameLayout[@content-desc=\"Listelerim\"]";
        driver.findElementByXPath(path).click();
        driver.manage().timeouts().implicitlyWait(5, TimeUnit.SECONDS);
    }

    @Override
    public void v_MostReaden() {
        String path = "/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.FrameLayout/androidx.drawerlayout.widget.DrawerLayout/android.widget.FrameLayout/android.widget.FrameLayout[1]/android.view.ViewGroup/android.view.ViewGroup/android.webkit.WebView/android.webkit.WebView/android.view.View/android.view.View[1]/android.view.View[1]";
        WebElement element = driver.findElement(By.xpath(path));
        String text = element.getAttribute("text");
        Assert.assertEquals(text, temp_text);
    }

    @Override
    public void v_Initial() {
        String activity = driver.currentActivity();
        Assert.assertEquals(activity, ".onboarding.InitialOnboardingActivity");
    }

    @Override
    public void e_NewEdge() {

    }

    @Override
    public void e_ClickSaved() {
        String path = "\t\n" +
                "/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.LinearLayout/android.view.ViewGroup/androidx.viewpager.widget.ViewPager/androidx.recyclerview.widget.RecyclerView/android.widget.FrameLayout/android.view.ViewGroup/android.view.ViewGroup/android.widget.LinearLayout/androidx.recyclerview.widget.RecyclerView/android.view.ViewGroup";
        driver.findElementByXPath(path).click();
        driver.manage().timeouts().implicitlyWait(5, TimeUnit.SECONDS);
    }
}
