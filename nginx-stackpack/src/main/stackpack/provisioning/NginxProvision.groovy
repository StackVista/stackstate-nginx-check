import com.stackstate.stackpack.ProvisioningScript
import com.stackstate.stackpack.ProvisioningContext
import com.stackstate.stackpack.ProvisioningIO
import com.stackstate.stackpack.Version

class NginxProvision extends ProvisioningScript {

  NginxProvision(ProvisioningContext context) {
      super(context)
  }

  @Override
  ProvisioningIO<scala.Unit> install(Map<String, Object> config) {

    def args = ['instanceName': config.nginx_instance]
    def templateArguments = [
                'nginxTopicName': NginxTopicName(config),
                'instanceId': context().instance().id(),
                'instanceName': config.nginx_instance
                ]
    templateArguments.putAll(config)

    return context().stackPack().importSnapshot("templates/nginx.stj", args) >>
           context().instance().importSnapshot("templates/nginx-instance-template.stj", templateArguments)
  }

  @Override
  ProvisioningIO<scala.Unit> upgrade(Map<String, Object> config, Version current) {
    return install(config)
  }

  @Override
  void waitingForData(Map<String, Object> config) {
    context().sts().onDataReceived(NginxTopicName(config), {
      context().sts().provisioningComplete()
    })
  }

  private def NginxTopicName(Map<String, Object> config) {
    def topic = config.nginx_instance
    return context().sts().createTopologyTopicName("nginx", topic)
  }
}
