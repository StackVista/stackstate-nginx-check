package com.stackstate.stackpack.nginx

import com.stackstate.stackpack.testkit.TestKit
import com.stackstate.stackpack.provisioning.helpers._
import org.scalatest.mockito.MockitoSugar
import org.scalatest.{Matchers, WordSpecLike}

import org.mockito.Matchers.{ eq => eql, _ }
import org.mockito.Mockito
import org.mockito.Mockito._
import org.mockito.invocation.InvocationOnMock

import scala.concurrent.duration._
import scala.collection.JavaConverters._

class NginxProvisioningTest extends WordSpecLike with Matchers {
  val testKit = new TestKit()
  import testKit._

  val config = Map[String, Object](
    "nginx_instance" -> "f4w001"
  )

  "The Nginx Provisioning" should {
    "import a template" in {
      stackPackPackage.preInstall(provisioningContext, config.asJava).run()
      stackPackPackage.install(provisioningContext, config.asJava).run()

      val (_, templateFile, args) = verifyTemplateImportedWithNamespace(provisioningContext.stackPack.namespace)
      args should not be empty
      templateFile shouldBe "templates/nginx.stj"

      val (_, instanceTemplateFile, instanceArgs) = verifyTemplateImportedWithNamespace(provisioningContext.instance.namespace)
      instanceArgs should not be empty
      instanceTemplateFile shouldBe "templates/nginx-instance-template.stj"
    }
  }
}
