package afg.tfg.restApi.model;

import javax.persistence.Column;
import javax.persistence.Entity;
import javax.persistence.Table;
import javax.validation.constraints.NotEmpty;

@Entity
@Table(name="companies")
public class Company extends User {
	
	@Column(name="name")
	@NotEmpty
	private String name;
	
	@Column(name="cif")
	@NotEmpty
	private String cif;
	
	@Column(name="telephone")
	@NotEmpty
	private String telephone;
	
	@Column(name="address")
	@NotEmpty
	private String address;
	
	@Column(name="account")
	@NotEmpty
	private String account;
	

	public String getName() {
		return name;
	}

	public void setName(String name) {
		this.name = name;
	}

	public String getCif() {
		return cif;
	}

	public void setCif(String cif) {
		this.cif = cif;
	}

	public String getAddress() {
		return address;
	}

	public void setAddress(String address) {
		this.address = address;
	}

	public String getAccount() {
		return account;
	}

	public void setAccount(String account) {
		this.account = account;
	}

	public String getTelephone() {
		return telephone;
	}

	public void setTelephone(String telephone) {
		this.telephone = telephone;
	}
	


}
