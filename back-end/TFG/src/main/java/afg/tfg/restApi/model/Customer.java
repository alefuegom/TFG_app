package afg.tfg.restApi.model;

import javax.persistence.Column;
import javax.persistence.Entity;
import javax.persistence.Table;
import javax.validation.constraints.NotEmpty;

@Entity
@Table(name="customers")
public class Customer extends User{
	
	@Column(name="name")
	@NotEmpty
	private String name;
	
	@Column(name="surname")
	@NotEmpty
	private String surname;
	
	@Column(name="dni")
	@NotEmpty
	private String dni;
	
	@Column(name="telephone")
	@NotEmpty
	private String telephone;
	
	@Column(name="address")
	@NotEmpty
	private String address;
	
	@Column(name="account")
	private String account;

	public String getName() {
		return name;
	}

	public void setName(String name) {
		this.name = name;
	}

	public String getSurname() {
		return surname;
	}

	public void setSurname(String surname) {
		this.surname = surname;
	}

	public String getDni() {
		return dni;
	}

	public void setDni(String dni) {
		this.dni = dni;
	}

	public String getTelephone() {
		return telephone;
	}

	public void setTelephone(String telephone) {
		this.telephone = telephone;
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
	
	

}
