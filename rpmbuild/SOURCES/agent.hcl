# Default config from package
vault {
  address = "https://127.0.0.1:8200"
  tls_skip_verify = false
}

auto_auth {
  method {
    type = "approle"

    config = {
      role_id_file_path = "/etc/vault/agent-roleid"
      secret_id_file_path = "/etc/vault/agent-secretid"
      remove_secret_id_file_after_reading = false
    }
  }

  sink {
    type = "file"

    config = {
      path = "/etc/vault/token"
      mode = 0755
    }
  }
}

template {
  source = "/etc/vault/server.conf.ctmpl"
  destination = "/etc/myapp/server.conf"
  command = "service myapp restart"
  perms = 0755
  error_on_missing_key = true
  backup = true
  wait = {
    min = 5
    max = 10
  }
}
