diff --git a/drivers/vhost/net.c b/drivers/vhost/net.c
index e158159671fa..18e205eeb9af 100644
--- a/drivers/vhost/net.c
+++ b/drivers/vhost/net.c
@@ -1414,10 +1414,6 @@ static int vhost_net_release(struct inode *inode, struct file *f)
 
 static struct socket *get_raw_socket(int fd)
 {
-	struct {
-		struct sockaddr_ll sa;
-		char  buf[MAX_ADDR_LEN];
-	} uaddr;
 	int r;
 	struct socket *sock = sockfd_lookup(fd, &r);
 
@@ -1430,11 +1426,7 @@ static struct socket *get_raw_socket(int fd)
 		goto err;
 	}
 
-	r = sock->ops->getname(sock, (struct sockaddr *)&uaddr.sa, 0);
-	if (r < 0)
-		goto err;
-
-	if (uaddr.sa.sll_family != AF_PACKET) {
+	if (sock->sk->sk_family != AF_PACKET) {
 		r = -EPFNOSUPPORT;
 		goto err;
 	}
